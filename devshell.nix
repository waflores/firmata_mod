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
      linuxKernel.kernels.linux_6_12  # The highest available at this nixpkgs
      # keep-sorted end
    ];
  }

# https://github.com/numtide/blueprint/blob/main/docs/content/guides/configuring_direnv.md
