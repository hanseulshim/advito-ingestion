import React from 'react'
import styled from 'styled-components'
import { Form, Icon, Input, Button } from 'antd'
import { useHistory, useLocation } from 'react-router'
import { useMutation } from '@apollo/client'
import queryString from 'query-string'
import advitoLogo from 'assets/advitoLogo.png'
import Footer from './Footer'
import { RESET_PASSWORD } from 'api'
import ErrorMessage from 'components/common/ErrorMessage'
import SuccessMessage from 'components/common/SuccessMessage'
import { SkeletonLoader } from 'components/common/Loader'
import { authClient } from 'index'

const Container = styled.div`
	width: 100%;
	height: 100%;
	position: absolute;
	left: 0;
	display: flex;
	flex-direction: column;
	align-items: center;
	background: ${props => props.theme.jungleMist};
`

const Logo = styled.img`
	margin: 3em 0 0 5em;
	max-width: 200px;
	width: 100%;
	align-self: flex-start;
`

const FormContainer = styled.div`
	padding: 2em 4em;
	width: 30%;
	max-width: 500px;
`

const Title = styled.div`
	font-size: 4em;
	text-align: center;
	margin: 2.5em 0 0.5em 0;
	color: ${props => props.theme.white};
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

const RestPassword = ({ form }) => {
	const history = useHistory()
	const location = useLocation()
	const [resetPassword, { loading, error, data }] = useMutation(
		RESET_PASSWORD,
		{
			client: authClient
		}
	)
	const params = queryString.parse(location.search)
	const { t: token = '' } = params

	const handleSubmit = async ({ password, confirmPassword }) => {
		try {
			await resetPassword({
				variables: { password, confirmPassword, token }
			})
		} catch (e) {
			console.error('Error in reset password form: ', e)
		}
	}

	return (
		<Container>
			<Logo src={advitoLogo} />
			<Title>Reset Password</Title>
			<FormContainer>
				<Form onFinish={handleSubmit}>
					{loading ? (
						<SkeletonLoader />
					) : (
						<>
							<Form.Item
								name="password"
								rules={[
									{ required: true, message: 'Please input your password!' }
								]}
							>
								<Input
									prefix={
										<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />
									}
									type="password"
									placeholder="Password"
								/>
							</Form.Item>
							<Form.Item
								name="confirmPassword"
								rules={[
									{ required: true, message: 'Please input your password!' }
								]}
							>
								<Input
									prefix={
										<Icon type="lock" style={{ color: 'rgba(0,0,0,.25)' }} />
									}
									type="password"
									placeholder="Confirm Password"
								/>
							</Form.Item>
						</>
					)}
					<Form.Item>
						<ButtonRow>
							<Button type="danger" htmlType="submit">
								Reset Password
							</Button>
							<Link onClick={() => history.push('/login')}>Back to Login</Link>
						</ButtonRow>
						{error && <ErrorMessage error={error} />}
						{data && <SuccessMessage message={'Password has been reset'} />}
					</Form.Item>
				</Form>
			</FormContainer>
			<Footer />
		</Container>
	)
}

export default RestPassword
