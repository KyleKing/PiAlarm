// Run with: node run-client.js --npm="start"
// or argument (--npm="run build"), etc

const args = require( 'minimist' )( process.argv.slice( 2 ) )
const opts = { cwd: 'client', shell: true, stdio: 'inherit' }
require( 'child_process' ).spawn( 'npm', [args.npm], opts )
