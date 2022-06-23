"""Local/On-premise."""
import subprocess
import typing
from typing import Dict, Iterator, List, Optional, Tuple

from sky import clouds

if typing.TYPE_CHECKING:
    # Renaming to avoid shadowing variables.
    from sky import resources as resources_lib


def _run_output(cmd):
    proc = subprocess.run(cmd,
                          shell=True,
                          check=True,
                          stderr=subprocess.PIPE,
                          stdout=subprocess.PIPE)
    return proc.stdout.decode('ascii')


@clouds.CLOUD_REGISTRY.register
class Local(clouds.Cloud):
    """A local/on-premise cloud as a set of local clusters.

    This Cloud has the following special treatment of Cloud concepts:

    - Catalog: Does not have service catalog.
    - Region: Only one region ('Local' region).
    - Cost: Treats all compute/egress as free.
    - Instance types: Only one instance type ('on-prem' instance type).
    - Cluster: Each Local cloud corresponds to exactly 1 cluster.
    - Credentials: No checking is done (in `sky check`) and users must
        provide their own credentials instead of Sky autogenerating
        cluster credentials.
    """

    LOCAL_REGION = clouds.Region('Local')
    _regions: List[clouds.Region] = [LOCAL_REGION]

    @classmethod
    def regions(cls):
        return cls._regions

    @classmethod
    def region_zones_provision_loop(
        cls,
        *,
        instance_type: Optional[str] = None,
        accelerators: Optional[Dict[str, int]] = None,
        use_spot: bool,
    ) -> Iterator[Tuple[clouds.Region, List[clouds.Zone]]]:
        del accelerators  # unused
        assert instance_type is None and not use_spot
        for region in cls.regions():
            yield region, region.zones

    #### Normal methods ####

    def instance_type_to_hourly_cost(self, instance_type: str,
                                     use_spot: bool) -> float:
        # On-prem machines on Sky are assumed free
        # (minus electricity/utility bills).
        return 0.0

    def accelerators_to_hourly_cost(self, accelerators,
                                    use_spot: bool) -> float:
        # Hourly cost of accelerators is 0 for local cloud.
        return 0

    def get_egress_cost(self, num_gigabytes: float) -> float:
        # Egress cost from a local cluster is assumed to be 0.
        return 0.0

    def __repr__(self):
        return 'Local'

    def is_same_cloud(self, other: clouds.Cloud) -> bool:
        # Returns true if the two clouds are the same cloud type
        # and has the matching cluster name.
        return isinstance(other, Local)

    @classmethod
    def get_default_instance_type(cls) -> str:
        # There is only "1" instance type for local cloud: on-prem
        return 'on-prem'

    @classmethod
    def get_accelerators_from_instance_type(
        cls,
        instance_type: str,
    ) -> Optional[Dict[str, int]]:
        # This function is not called, as local cloud does not have service
        # catalog.
        raise NotImplementedError

    def make_deploy_resources_variables(self,
                                        resources: 'resources_lib.Resources'):
        return {}

    def get_feasible_launchable_resources(self,
                                          resources: 'resources_lib.Resources'):
        # The entire local cluster's resources is considered launchable, as the
        # check for task resources is deferred later.
        # The check for task resources meeting cluster resources is run in
        # cloud_vm_ray_backend._check_task_resources_smaller_than_cluster.
        return [resources], []

    def check_credentials(self) -> Tuple[bool, Optional[str]]:
        # Cloud clouds.Local is not called in `sky check`
        # (not part of global registry).
        return True, None

    def get_credential_file_mounts(self) -> Dict[str, str]:
        # Credentials are not autogenerated by Sky.
        # Credentials are instead provided by the user, hence this method
        # returns an empty dict.
        return {}

    def instance_type_exists(self, instance_type: str) -> bool:
        # Checks if instance_type matches on-prem, the only instance type for
        # local cloud.
        return instance_type == self.get_default_instance_type()

    def region_exists(self, region: str) -> bool:
        # Returns true if the region name is same as Local cloud's
        # one and only region: 'Local'.
        return region == Local.LOCAL_REGION.name