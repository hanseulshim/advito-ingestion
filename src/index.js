import React from 'react'
import ReactDOM from 'react-dom'
import App from './App'
import * as serviceWorker from './serviceWorker'
import ApolloClient from 'apollo-boost'
import { ApolloProvider } from '@apollo/react-hooks'
import { Router } from 'react-router-dom'
import history from './history'
import { getToken, removeUser, getApi } from './helper'

const client = new ApolloClient({
  uri: getApi(),
  request: operation => {
    const sessiontoken = getToken()
    if (sessiontoken) {
      operation.setContext({
        headers: {
          sessiontoken
        }
      })
    }
  },
  onError: ({ graphQLErrors }) => {
    if (graphQLErrors) {
      graphQLErrors.forEach(({ extensions }) => {
        if (extensions.code === 401) {
          removeUser()
        }
      })
    }
  }
})

ReactDOM.render(
  <ApolloProvider client={client}>
    <Router history={history}>
      <App />
    </Router>
  </ApolloProvider>,
  document.getElementById('root')
)

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister()
