// Entry Point for Server Configuration

// Configure logging
const debug = require( 'debug' )
debug.enable( 'App:*' )

// Launch the server instance
require( './server/Server.js' )
