import gql from 'graphql-tag'

export const SEND_RESET_PASSWORD = gql`
	mutation sendResetPasswordEmail($email: String!) {
		sendResetPasswordEmail(email: $email)
	}
`
export const LOGIN = gql`
	mutation login($username: String!, $password: String!) {
		login(username: $username, password: $password) {
			id
			displayName
			clientId
			sessionToken
			roleIds
		}
	}
`
export const LOGOUT = gql`
	mutation logout($sessionToken: String!) {
		logout(sessionToken: $sessionToken)
	}
`
export const RESET_PASSWORD = gql`
	mutation resetPassword(
		$token: String!
		$password: String!
		$confirmPassword: String!
	) {
		resetPassword(
			token: $token
			password: $password
			confirmPassword: $confirmPassword
		)
	}
`
