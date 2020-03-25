import React, { useState } from 'react'
import styled from 'styled-components'
import { Form, Input, Button } from 'antd'
import { UserOutlined, LockOutlined } from '@ant-design/icons'
import { Redirect } from 'react-router-dom'
import { useMutation } from '@apollo/client'
import advitoLogo from 'assets/advitoLogo.png'
import Footer from './Footer'
import ResetPasswordModal from './ResetPasswordModal'
import { LOGIN } from 'api'
import ErrorMessage from 'components/common/ErrorMessage'
import SuccessMessage from 'components/common/SuccessMessage'
import { SkeletonLoader } from 'components/common/Loader'
import { setUser } from 'helper'
import { authClient } from 'index'

const Container = styled.div`
	width: 100%;
	height: 100%;
	min-height: 1000px;
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

const Login = () => {
	const [visible, setVisible] = useState(false)
	const [login, { loading, error, data }] = useMutation(LOGIN, {
		client: authClient
	})

	const handleSubmit = async ({ username, password }) => {
		try {
			await login({
				variables: { username, password }
			})
		} catch (e) {
			console.error('Error in login form: ', e)
		}
	}

	if (data) {
		setUser(data.login)
		return <Redirect to="/" />
	}

	return (
		<Container>
			<Logo>
				<img src={advitoLogo} alt="logo" />
			</Logo>
			<Title>
				Welcome to the <br /> Advito Ingestion Console
			</Title>
			<FormContainer>
				<Form onFinish={handleSubmit}>
					{loading ? (
						<SkeletonLoader />
					) : (
						<>
							<Form.Item
								name="username"
								rules={[
									{ required: true, message: 'Please input your username!' },
									{
										type: 'email',
										message: 'The input is not a valid email!'
									}
								]}
							>
								<Input prefix={<UserOutlined />} placeholder="Username" />
							</Form.Item>
							<Form.Item
								name="password"
								rules={[
									{ required: true, message: 'Please input your password!' }
								]}
							>
								<Input
									prefix={<LockOutlined />}
									type="password"
									placeholder="Password"
								/>
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

export default Login
