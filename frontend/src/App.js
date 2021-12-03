import React from 'react'
import styled from 'styled-components';
import { Title } from './components/shared';
import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';

const Layout = styled.div`
  with: 100%;
  height: 100%;
  margin: 0;
  padding: 0;

  display: grid;
  grid-template-areas: 
    "header"
    "content"
    "footer";
  grid-template-rows: 75px auto 50px;
  grid-template-columns: auto;
`;

const Header = styled.header`
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 1em;
  background-color: rgb(129, 223, 229);
  color: white;
`;

const Content = styled.div`
  width: 100%;
  height: 100%;
`;

const Footer = styled.footer`
  display: flex;
  align-items: center;
  with: 100%;
  height: 100%;
  padding: 1em;
  background-color: rgb(129, 223, 229);
  color: white;
`;

const App = () => {
  return (
    <Layout>
      <Header>
        <Title>Garbage detector</Title>
      </Header>
      <Content>
        <Routes>
          <Route path='dashboard/' element={<Dashboard />} />
          <Route path='/' element={<Navigate to='dashboard/' />} />
        </Routes>
      </Content>
      <Footer>Powered by NoName team.</Footer>
    </Layout>
  );
};

export default App;
