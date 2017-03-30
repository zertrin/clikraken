-- Setting up
-----------------------------------------------------------------------------------
  $ export CLIKRAKEN_SETTINGS_BASEPATH="$CRAMTMP/.config/clikraken"
  $ export CLIKRAKEN_USER_SETTINGS_PATH="$CLIKRAKEN_SETTINGS_BASEPATH/settings.ini"
  $ export CLIKRAKEN_API_KEYFILE="$CLIKRAKEN_SETTINGS_BASEPATH/kraken.key"
  $ mkdir -p $CLIKRAKEN_SETTINGS_BASEPATH
  $ echo -e "dummy\nkey" > $CLIKRAKEN_API_KEYFILE
  $ cat $TESTDIR/settings_examples/settings.ini.generated > $CLIKRAKEN_USER_SETTINGS_PATH

-- Test
-----------------------------------------------------------------------------------
  $ clikraken -V
  clikraken version: .+ (re)
