import { Menu } from 'antd';
import { BarsOutlined, FileZipFilled, FireFilled, HomeOutlined, SettingOutlined } from '@ant-design/icons';

const MenuList = () => {
    return (
        <Menu theme='dark' mode='inline' className='menu-bar'>
            <Menu.Item key="home" icon={<HomeOutlined />}>
                Home
            </Menu.Item>
            <Menu.Item key="fires" icon={<FireFilled />}>
                Fires
            </Menu.Item>
            <Menu.Item key="zones" icon={<FileZipFilled />}>
                Zones
            </Menu.Item>
            <Menu.Item key="settings" icon={<SettingOutlined />}>
                Settings
            </Menu.Item>
            <Menu.SubMenu key="tasks" icon={<BarsOutlined />} title="Tasks">
    <Menu.Item key="task-1">Task 1</Menu.Item>
    <Menu.Item key="task-2">Task 2</Menu.Item>
    <Menu.SubMenu key="subtasks" title="Subtasks">
        <Menu.Item key="subtask-1">Subtask 1</Menu.Item>
        <Menu.Item key="subtask-2">Subtask 2</Menu.Item>
    </Menu.SubMenu>
</Menu.SubMenu>


            
        </Menu>
    );
};

export default MenuList;
