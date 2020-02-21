import gql from 'graphql-tag'

export const UPLOAD_FILE = gql`
  mutation uploadFile($fileName: String!, $base64: String!) {
    uploadFile(fileName: $fileName, base64: $base64)
  }
`
