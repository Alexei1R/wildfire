// App.js
import React from "react";
import { Layout } from "antd";
import Logo from "./components/Logo";
import MenuList from "./components/MenuList";
import GoogleMap from "./components/GoogleMap";

const { Sider, Content } = Layout;

const App = () => {
  return (
    <Layout style={{ height: "100vh" }}>
      <Sider className="sidebar" width={200}>
        <Logo />
        <MenuList />
      </Sider>
      <Content className="main-content">
        <GoogleMap />
      </Content>
    </Layout>
  );
};

export default App;
