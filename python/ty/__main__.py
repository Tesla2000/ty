from __future__ import annotations

import os
import sys
import sysconfig


def find_ty_bin() -> str:
    """Return the ty binary path."""

    ty_exe = "ty" + sysconfig.get_config_var("EXE")

    scripts_path = os.path.join(sysconfig.get_path("scripts"), ty_exe)
    if os.path.isfile(scripts_path):
        return scripts_path

    if sys.version_info >= (3, 10):
        user_scheme = sysconfig.get_preferred_scheme("user")
    elif os.name == "nt":
        user_scheme = "nt_user"
    elif sys.platform == "darwin" and sys._framework:
        user_scheme = "osx_framework_user"
    else:
        user_scheme = "posix_user"

    user_path = os.path.join(sysconfig.get_path("scripts", scheme=user_scheme), ty_exe)
    if os.path.isfile(user_path):
        return user_path

    # Search in `bin` adjacent to package root (as created by `pip install --target`).
    pkg_root = os.path.dirname(os.path.dirname(__file__))
    target_path = os.path.join(pkg_root, "bin", ty_exe)
    if os.path.isfile(target_path):
        return target_path

    # Search for pip-specific build environments.
    #
    # Expect to find ty in <prefix>/pip-build-env-<rand>/overlay/bin/ty
    # Expect to find a "normal" folder at <prefix>/pip-build-env-<rand>/normal
    #
    # See: https://github.com/pypa/pip/blob/102d8187a1f5a4cd5de7a549fd8a9af34e89a54f/src/pip/_internal/build_env.py#L87
    paths = os.environ.get("PATH", "").split(os.pathsep)
    if len(paths) >= 2:

        def get_last_three_path_parts(path: str) -> list[str]:
            """Return a list of up to the last three parts of a path."""
            parts = []

            while len(parts) < 3:
                head, tail = os.path.split(path)
                if tail or head != path:
                    parts.append(tail)
                    path = head
                else:
                    parts.append(path)
                    break

            return parts

        maybe_overlay = get_last_three_path_parts(paths[0])
        maybe_normal = get_last_three_path_parts(paths[1])
        if (
            len(maybe_normal) >= 3
            and maybe_normal[-1].startswith("pip-build-env-")
            and maybe_normal[-2] == "normal"
            and len(maybe_overlay) >= 3
            and maybe_overlay[-1].startswith("pip-build-env-")
            and maybe_overlay[-2] == "overlay"
        ):
            # The overlay must contain the ty binary.
            candidate = os.path.join(paths[0], ty_exe)
            if os.path.isfile(candidate):
                return candidate

    raise FileNotFoundError(scripts_path)


def main():
    ty = os.fsdecode(find_ty_bin())
    if sys.platform == "win32":
        import subprocess

        completed_process = subprocess.run([ty, *sys.argv[1:]])
        sys.exit(completed_process.returncode)
    else:
        os.execvp(ty, [ty, *sys.argv[1:]])


if __name__ == "__main__":
    main()
