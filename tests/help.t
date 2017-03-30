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
  $ clikraken -h
  usage: clikraken [-h] [-V] [--raw] [--cron]
                   {generate_settings,ticker,t,depth,d,last_trades,lt,balance,bal,place,p,cancel,x,olist,ol,clist,cl}
                   ...
  
  clikraken - Command line client for the Kraken exchange
  
  positional arguments:
    {generate_settings,ticker,t,depth,d,last_trades,lt,balance,bal,place,p,cancel,x,olist,ol,clist,cl}
                          available subcommands
      generate_settings   [clikraken] Print default settings.ini to stdout
      ticker (t)          [public] Get the Ticker
      depth (d)           [public] Get the current market depth data
      last_trades (lt)    [public] Get the last trades
      balance (bal)       [private] Get your current balance
      place (p)           [private] Place an order
      cancel (x)          [private] Cancel orders
      olist (ol)          [private] Get a list of your open orders
      clist (cl)          [private] Get a list of your closed orders
  
  optional arguments:
    -h, --help            show this help message and exit
    -V, --version         show program version
    --raw                 output raw json results from the API
    --cron                activate cron mode (tone down errors due to timeouts
                          or unavailable Kraken service)
  
  To get help about a subcommand use: clikraken SUBCOMMAND --help
  For example:
      clikraken place --help
  
  Current default currency pair: XETHZEUR.
  
  Create or edit the setting file *settings.ini to change it. (glob)
  If the setting file doesn't exist yet, you can create one by doing:
      clikraken generate_settings > *settings.ini (glob)
  
  You can also set the CLIKRAKEN_DEFAULT_PAIR environment variable
  which has precedence over the settings from the settings file.
