import gql from 'graphql-tag'

export const UPLOAD_FILE = gql`
	mutation uploadFile(
		$clientId: Int!
		$sourceId: Int!
		$dataStartDate: Date!
		$dataEndDate: Date!
		$fileName: String!
		$fileSize: Int!
		$base64: String!
	) {
		uploadFile(
			clientId: $clientId
			sourceId: $sourceId
			dataStartDate: $dataStartDate
			dataEndDate: $dataEndDate
			fileName: $fileName
			fileSize: $fileSize
			base64: $base64
		)
	}
`
