// Wrap common NedB functions as promises
// TODO: Is there an easier way to wrap NedB as promises?

function count( db, query ) {
	return new Promise( ( resolve, reject ) => {
		db.count( query, ( err, countMatches ) => {
			if ( err )
				reject( err )
			else
				resolve( countMatches )
		} )
	} )
}
function find( db, query ) {
	return new Promise( ( resolve, reject ) => {
		db.find( query, ( err, docs ) => {
			if ( err )
				reject( err )
			else
				resolve( docs )
		} )
	} )
}
function findOne( db, query ) {
	return new Promise( ( resolve, reject ) => {
		db.findOne( query, ( err, doc ) => {
			if ( err )
				reject( err )
			else
				resolve( doc )
		} )
	} )
}
function insert( db, doc ) {
	return new Promise( ( resolve, reject ) => {
		db.insert( doc, ( err, finalDoc ) => {
			if ( err )
				reject( err )
			else
				resolve( finalDoc )
		} )
	} )
}
function remove( db, query ) {
	return new Promise( ( resolve, reject ) => {
		db.remove( query, ( err, numRemoved ) => {
			if ( err )
				reject( err )
			else
				resolve( numRemoved )
		} )
	} )
}
function update( db, query, newDoc, options ) {
	return new Promise( ( resolve, reject ) => {
		db.update( query, newDoc, options, ( err, numAffected, affectedDocuments, upsert ) => {
			if ( err )
				reject( err )
			else
				resolve( { affectedDocuments, numAffected, upsert } )

		} )
	} )
}


module.exports = {
	count,
	find,
	findOne,
	insert,
	remove,
	update,
}
