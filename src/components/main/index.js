import React, { useState, useEffect } from 'react'
import styled from 'styled-components'
import Sidebar from 'components/sidebar'
import Form from './form'
import advitoLogo from 'assets/advitoLogo.png'
import bcdLogo from 'assets/bcdLogo.png'
import { useHistory, useLocation } from 'react-router'
import queryString from 'query-string'
import isEmpty from 'lodash.isempty'
import { getUser } from 'helper'

const MainContainer = styled.div`
	width: 100%;
	min-height: 100%;
	display: flex;
`

const FormContainer = styled.div`
	display: flex;
	flex: 4;
	flex-direction: column;
	padding: ${props => props.theme.verticalSpace}
		${props => props.theme.horizontalSpace};
`

const Header = styled.div`
	margin-bottom: ${props => props.theme.verticalSpace};
`

const Main = () => {
	const [bcd, setBcd] = useState(false)
	const location = useLocation()
	const history = useHistory()
	const params = queryString.parse(location.search)
	useEffect(() => {
		if (!isEmpty(params)) {
			history.push('/')
		}
		const user = getUser()
		if (user.bcd) {
			setBcd(user.bcd)
		}
	}, [params])
	return (
		<>
			<MainContainer>
				<Sidebar />
				<FormContainer>
					<Header>
						<img src={bcd ? bcdLogo : advitoLogo} alt="advito logo" />
					</Header>
					<Form />
				</FormContainer>
			</MainContainer>
		</>
	)
}

export default Main
