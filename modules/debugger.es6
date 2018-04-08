/**
 * initialize debugger
 */

const clc = require( 'cli-color' )
const debug = require( 'debug' )
const fs = require( 'fs' )

module.exports = {
  error: clc.red.bold,
  exists( filename, cb ) {
    fs.access( filename, cb )
  },
  existsSync( filename ) {
    try {
      fs.accessSync( filename )
      return true
    } catch ( ex ) {
      return false
    }
  },
  ignore: clc.xterm( 8 ),
  info: clc.blue,
  init: ( app ) => {
    if ( process.env.VERBOSE !== 'false' ) debug.enable( 'app:*' )
    return debug( `app:${app}` )
  },
  warn: clc.yellow,
}
