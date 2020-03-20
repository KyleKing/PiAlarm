// Entry Point for Server Configuration

// Configure logging
const debug = require( 'debug' )
debug.enable( 'App:*' )

// Initialize the database and launch server
require( './server/Database.js' )
require( './server/Server.js' )
