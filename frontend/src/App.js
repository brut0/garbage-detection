import React from 'react'
import styled from 'styled-components';
import { Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import { Button, PageHeader } from 'antd';
import { observer } from 'mobx-react-lite';

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
  color: black;
`;

const App = () => {
  return (
    <Layout>
      <PageHeader 
        title='Garbage detector'
        extra={[
          <Button href='/grafana'>Grafana</Button>,
          <Button href='/hitmap'>Тепловая карта</Button>
        ]}
      />
      <Content>
        <Routes>
          <Route path='dashboard/' element={<Dashboard />} />
          <Route path='*' element={<Navigate to='dashboard/' />} />
        </Routes>
      </Content>
      <Footer>Powered by NoName team.</Footer>
    </Layout>
  );
};

export default observer(App);
