# Upgrade detection is a mess. It is often difficult to tell, especially from
# the postinstall script, so we use the package-upgrade.txt file to remember.

case "$PKG_TYPE" in
  depot|deb|bff)
    if [ "$SCRIPT_TYPE" = "preinstall" ]; then
      if native_is_upgrade; then
        mkdir -p "$PREFIX"
        echo "File used by CFEngine during package upgrade. Can be safely deleted." > "$PREFIX/package-upgrade.txt"
      else
        rm -f "$PREFIX/package-upgrade.txt"
      fi
      alias is_upgrade='native_is_upgrade'
    elif [ "$SCRIPT_TYPE" = "postinstall" ]; then
      if [ -f "$PREFIX/package-upgrade.txt" ]; then
        rm -f "$PREFIX/package-upgrade.txt"
        alias is_upgrade='true'
      else
        alias is_upgrade='false'
      fi
    fi
    ;;
esac
