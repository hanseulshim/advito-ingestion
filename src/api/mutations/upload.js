import gql from 'graphql-tag'

export const UPLOAD_FILE = gql`
	mutation uploadFile(
		$clientId: Int!
		$advitoApplicationId: Int!
		$sourceId: Int!
		$dataStartDate: Date!
		$dataEndDate: Date!
		$fileName: String!
		$fileSize: Int!
		$key: String!
	) {
		uploadFile(
			clientId: $clientId
			advitoApplicationId: $advitoApplicationId
			sourceId: $sourceId
			dataStartDate: $dataStartDate
			dataEndDate: $dataEndDate
			fileName: $fileName
			fileSize: $fileSize
			key: $key
		)
	}
`
