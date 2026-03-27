# Using mkShell from nixpkgs
{
  pkgs,
  ...
}:
pkgs.mkShell.override
  {
    # stdenv = pkgs.clangStdenv;
  }
  rec {
    name = "firmata-shell";
    # shellHook = ''
    # export JAVA_HOME=${pkgs.jdk21_headless.home}
    # '';

    packages = with pkgs; [
      # keep-sorted start block=yes case=no
      bashInteractive
      bazel-buildtools
      bazelisk
      cacert
      clang
      clang-tools
      clang-uml
      compiledb
      jdk21_headless
      linuxKernel.kernels.linux_6_12 # The highest available at this nixpkgs
      # keep-sorted end
    ];
  }

# https://github.com/numtide/blueprint/blob/main/docs/content/guides/configuring_direnv.md
