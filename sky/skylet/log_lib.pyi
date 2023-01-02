from sky import sky_logging as sky_logging
from sky.skylet import constants as constants, job_lib as job_lib
from sky.utils import log_utils as log_utils
import typing
from typing import Dict, List, Optional, Tuple, Union
from typing_extensions import Literal


def process_subprocess_stream(
        proc,
        log_path: str,
        stream_logs: bool,
        start_streaming_at: str = ...,
        end_streaming_at: Optional[str] = ...,
        skip_lines: Optional[List[str]] = ...,
        replace_crlf: bool = ...,
        line_processor: Optional[log_utils.LineProcessor] = ...,
        streaming_prefix: Optional[str] = ...) -> Tuple[str, str]:
    ...


@typing.overload
def run_with_log(cmd: Union[List[str], str],
                 log_path: str,
                 *,
                 require_outputs: Literal[False] = False,
                 stream_logs: bool = ...,
                 start_streaming_at: str = ...,
                 end_streaming_at: Optional[str] = ...,
                 skip_lines: Optional[List[str]] = ...,
                 shell: bool = ...,
                 with_ray: bool = ...,
                 process_stream: bool = ...,
                 line_processor: Optional[log_utils.LineProcessor] = ...,
                 streaming_prefix: Optional[str] = ...,
                 ray_job_id: Optional[str] = ...,
                 use_sudo: bool = ...,
                 **kwargs) -> int:
    ...


@typing.overload
def run_with_log(cmd: Union[List[str], str],
                 log_path: str,
                 *,
                 require_outputs: Literal[True],
                 stream_logs: bool = ...,
                 start_streaming_at: str = ...,
                 end_streaming_at: Optional[str] = ...,
                 skip_lines: Optional[List[str]] = ...,
                 shell: bool = ...,
                 with_ray: bool = ...,
                 process_stream: bool = ...,
                 line_processor: Optional[log_utils.LineProcessor] = ...,
                 streaming_prefix: Optional[str] = ...,
                 ray_job_id: Optional[str] = ...,
                 use_sudo: bool = ...,
                 **kwargs) -> Tuple[int, str, str]:
    ...


@typing.overload
def run_with_log(cmd: Union[List[str], str],
                 log_path: str,
                 *,
                 require_outputs: bool = False,
                 stream_logs: bool = ...,
                 start_streaming_at: str = ...,
                 end_streaming_at: Optional[str] = ...,
                 skip_lines: Optional[List[str]] = ...,
                 shell: bool = ...,
                 with_ray: bool = ...,
                 process_stream: bool = ...,
                 line_processor: Optional[log_utils.LineProcessor] = ...,
                 streaming_prefix: Optional[str] = ...,
                 ray_job_id: Optional[str] = ...,
                 use_sudo: bool = ...,
                 **kwargs) -> Union[int, Tuple[int, str, str]]:
    ...


def make_task_bash_script(codegen: str,
                          env_vars: Optional[Dict[str, str]] = ...) -> str:
    ...


def add_ray_env_vars(
        env_vars: Optional[Dict[str, str]] = ...) -> Dict[str, str]:
    ...


def run_bash_command_with_log(bash_command: str,
                              log_path: str,
                              job_owner: str,
                              job_id: int,
                              env_vars: Optional[Dict[str, str]] = ...,
                              stream_logs: bool = ...,
                              with_ray: bool = ...,
                              use_sudo: bool = ...):
    ...


def tail_logs(job_owner: str,
              job_id: int,
              log_dir: Optional[str],
              spot_job_id: Optional[int] = ...,
              follow: bool = ...) -> None:
    ...