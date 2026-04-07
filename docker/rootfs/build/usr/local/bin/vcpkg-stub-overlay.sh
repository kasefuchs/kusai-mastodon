#!/usr/bin/env bash
set -euo pipefail

OVERLAY="${VCPKG_OVERLAY_PORTS:-./overlay-ports}"

for PKG; do
  mkdir -p "$OVERLAY/$PKG"

  echo "set(VCPKG_POLICY_EMPTY_PACKAGE enabled)" >"$OVERLAY/$PKG/portfile.cmake"
  printf '{"name":"%s","version":"1.0.0"}' "$PKG" >"$OVERLAY/$PKG/vcpkg.json"
done
