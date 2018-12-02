import Client from './Client'
import Mutation from './Mutation'
import auth from './auth'

// Test GraphQL requests
// auth( 'BadPass', () => '' )
auth( 'SecretPass',  () => {
	Mutation.setMessage( 'DeepThoughts', 'How much wood can a wood chuck...' )
	setTimeout( Client.rollDice, 200, 3, 6 )
} )
