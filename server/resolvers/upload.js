export default {
  Mutation: {
    uploadFile(_, { fileName, base64 }) {
      console.log(fileName);
      return true;
    }
  }
}
