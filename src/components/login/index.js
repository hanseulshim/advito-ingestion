import React, { useState } from 'react'
import PropTypes from 'prop-types'
import styled from 'styled-components'
import { Form, Icon, Input, Button } from 'antd'
import { Redirect } from 'react-router-dom'
import { useMutation } from '@apollo/react-hooks'
import advitoLogo from 'assets/advitoLogo.png'
import Footer from './Footer'
import ResetPasswordModal from './ResetPasswordModal'
import { LOGIN } from 'api'
import ErrorMessage from 'components/common/ErrorMessage'
import SuccessMessage from 'components/common/SuccessMessage'
import { SkeletonLoader } from 'components/common/Loader'
import { setUser } from 'helper'

const Container = styled.div`
  width: 100%;
  height: 100vh;
  background: ${props => props.theme.jungleMist};
  display: flex;
  flex-direction: column;
  align-items: center;
`

const Logo = styled.div`
  display: flex;
  width: 100%;
  padding: 2em;
  > img {
    max-width: 200px;
    margin-left: 2em;
  }
`

const Title = styled.div`
  font-size: 4em;
  text-align: center;
  color: ${props => props.theme.white};
  line-height: 1.25;
  margin-top: 2em;
`

const FormContainer = styled.div`
  padding: 2em 4em;
  width: 30%;
  max-width: 500px;
`

const ButtonRow = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1em;
`

const Link = styled.div`
  color: ${props => props.theme.white};
  cursor: pointer;
  :hover {
    opacity: 0.7;
  }
`

const Login = ({ form }) => {
  const [visible, setVisible] = useState(false)
  const [login, { loading, error, data }] = useMutation(LOGIN)

  const handleSubmit = e => {
    e.preventDefault()
    form.validateFields(async (err, { username, password }) => {
      if (!err) {
        try {
          await login({
            variables: { username, password }
          })
        } catch (e) {
          console.error('Error in login form: ', e)
        }
      }
    })
  }

  if (data) {
    setUser(data.login)
    return <Redirect to="/" />
  }

  const { getFieldDecorator } = form
  return (
    <Container>
      <Logo>
        <img src={advitoLogo} alt="logo" />
      </Logo>
      <Title>
        Welcome to the <br /> Advito Ingestion Console
      </Title>
      <FormContainer>
        <Form onSubmit={handleSubmit}>
          {loading ? (
            <SkeletonLoader />
          ) : (
            <>
              <Form.Item>
                {getFieldDecorator('username', {
                  rules: [
                    { required: true, message: 'Please input your username!' },
                    {
                      type: 'email',
                      message: 'The input is not a valid email!'
                    }
                  ]
                })(
                  <Input
                    prefix={
                      <Icon type="user" style={{ color: 'rgba(0,0,0,.25)' }} />
                    }
                    placeholder="Username"
                  />
                )}
              </Form.Item>
              <Form.Item>
                {getFieldDecorator('password', {
                  rules: [
                    { required: true, message: 'Please input your password!' }
                  ]
                })(
                  <Input
                    prefix={
                      <Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />
                    }
                    type="password"
                    placeholder="Password"
                  />
                )}
              </Form.Item>
            </>
          )}
          <Form.Item>
            <ButtonRow>
              <Button type="danger" htmlType="submit">
                Log in
              </Button>
              <Link onClick={() => setVisible(true)}>Forgot Password?</Link>
            </ButtonRow>
            {error && <ErrorMessage error={error} />}
            {data && <SuccessMessage message={'Success!'} />}
          </Form.Item>
        </Form>
      </FormContainer>
      <ResetPasswordModal visible={visible} setVisible={setVisible} />
      <Footer />
    </Container>
  )
}

const LoginForm = Form.create({ name: 'login' })(Login)

Login.propTypes = {
  form: PropTypes.object.isRequired
}

export default LoginForm
