import React from 'react'
import PropTypes from 'prop-types'
import { ThemeProvider } from 'styled-components'
import { Route, Switch, Redirect } from 'react-router-dom'
import theme from 'styles/variables'
import GlobalStyle from 'styles/GlobalStyle'
import Login from 'components/login'
// import Main from 'components/Main'

import { library } from '@fortawesome/fontawesome-svg-core'
import { fas } from '@fortawesome/free-solid-svg-icons'

library.add(fas)

// const PrivateRoute = ({ component: Component }) => (
//   <Route
//     render={() => (getToken() ? <Component /> : <Redirect to="/login" />)}
//   />
// )

const App = () => (
  <ThemeProvider theme={theme}>
    <GlobalStyle />
    <Switch>
      <Route path="/" component={Login} />
    </Switch>
  </ThemeProvider>
)

// PrivateRoute.propTypes = {
//   component: PropTypes.func.isRequired
// }

export default App
