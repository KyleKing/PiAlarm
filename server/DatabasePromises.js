// Wrap common NedB functions as promises
// TODO: There has to be an easier way to do this

function count( db, query ) {
	return new Promise( ( resolve, reject ) => {
		db.count( query, ( err, count ) => {
			if ( err )
				reject( err )
			else
				resolve( count )
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
		db.insert( doc, ( err, doc ) => {
			if ( err )
				reject( err )
			else
				resolve( doc )
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
function update( db, query, update, options ) {
	return new Promise( ( resolve, reject ) => {
		db.update( query, update, options, ( err, numAffected, affectedDocuments, upsert ) => {
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
