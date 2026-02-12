"""
HuaiMS - Converted from Java source
Original: gui/HuaiMS.java
Package: gui
"""

from concurrent.futures import Future
from pymysql import Connection
from pymysql import Error
from pymysql.cursors import Cursor
from typing import List
from typing import Optional, Any
import logging
import pymysql
import sched
import threading
import time
import tkinter

# Internal module imports
# from client.LoginCrypto import *  # TODO: import specific classes
# from client.MapleCharacter import *  # TODO: import specific classes
# from client.inventory.Equip import *  # TODO: import specific classes
# from client.inventory.ItemFlag import *  # TODO: import specific classes
# from client.inventory.MapleInventoryType import *  # TODO: import specific classes
# from constants.GameConstants import *  # TODO: import specific classes
# from constants.ServerConstants import *  # TODO: import specific classes
# from database.DatabaseConnection import *  # TODO: import specific classes
# from handling.RecvPacketOpcode import *  # TODO: import specific classes
# from handling.SendPacketOpcode import *  # TODO: import specific classes
# from handling.channel.ChannelServer import *  # TODO: import specific classes
# from handling.login.handler.AutoRegister import *  # TODO: import specific classes
# from handling.world.World import *  # TODO: import specific classes
# from scripting.PortalScriptManager import *  # TODO: import specific classes
# from scripting.ReactorScriptManager import *  # TODO: import specific classes
# from server.CashItemFactory import *  # TODO: import specific classes
# from server.MapleInventoryManipulator import *  # TODO: import specific classes
# from server.MapleItemInformationProvider import *  # TODO: import specific classes
# from server.MapleShopFactory import *  # TODO: import specific classes
# from server.ShutdownServer import *  # TODO: import specific classes
# from server.Start import *  # TODO: import specific classes
# from server.Timer import *  # TODO: import specific classes
# from server.life.MapleMonsterInformationProvider import *  # TODO: import specific classes
# from server.quest.MapleQuest import *  # TODO: import specific classes
# from tools.MaplePacketCreator import *  # TODO: import specific classes


class HuaiMS(JFrame):
    """
    Class HuaiMS
    Extends: JFrame
    """

    def __init__(self):
        self.minutesLeft = 0
        self.canvas1 = None
        self.chatLog = None
        self.checkbox1 = None
        self.jButton1 = None
        self.jButton10 = None
        self.jButton11 = None
        self.jButton12 = None
        self.jButton13 = None
        self.jButton14 = None
        self.jButton15 = None
        self.jButton16 = None
        self.jButton17 = None
        self.jButton18 = None
        self.jButton19 = None
        self.jButton2 = None
        self.jButton20 = None
        self.jButton21 = None
        self.jButton22 = None
        self.jButton23 = None
        self.jButton3 = None
        self.jButton4 = None
        self.jButton5 = None
        self.jButton6 = None
        self.jButton7 = None
        self.jButton8 = None
        self.jButton9 = None
        self.jLabel1 = None
        self.jLabel2 = None
        self.jLabel3 = None
        self.jLabel4 = None
        self.jLabel5 = None
        self.jLabel6 = None
        self.jLabel7 = None
        self.jPanel1 = None
        self.jPanel2 = None
        self.jPanel3 = None
        self.jPanel5 = None
        self.jPanel6 = None
        self.jPanel7 = None
        self.minutesLeft = 0
        icon = ImageIcon(self.getClass().getClassLoader().getResource("gui/Icon.png"))
        self.setIconImage(icon.getImage())
        # switch (GameConstants.game):
            # case 0:
                self.setTitle("服务端-079V6控制台")
                break
            # default:
                self.setTitle("服务端-控制台")
                break
        self.initComponents()

    # Static initializer
    # HuaiMS.instance = HuaiMS()
    # HuaiMS.ts = None
    # HuaiMS.t = None


    @classmethod
    def get_instance(cls) -> "Any":
        if not hasattr(cls, "_instance") or cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def initComponents(self) -> None:
        self.canvas1 = Canvas()
        self.jScrollPane1 = JScrollPane()
        self.chatLog = JTextPane()
        self.jTabbedPane2 = JTabbedPane()
        self.jPanel5 = JPanel()
        self.jButton10 = JButton()
        self.jTextField22 = JTextField()
        self.jButton16 = JButton()
        self.jButton22 = JButton()
        self.jButton23 = JButton()
        self.jScrollPane2 = JScrollPane()
        self.jTextArea1 = JTextArea()
        self.jPanel7 = JPanel()
        self.jButton7 = JButton()
        self.jButton8 = JButton()
        self.jLabel2 = JLabel()
        self.jPanel6 = JPanel()
        self.jButton9 = JButton()
        self.jButton1 = JButton()
        self.jButton5 = JButton()
        self.jButton4 = JButton()
        self.jButton3 = JButton()
        self.jButton2 = JButton()
        self.jLabel1 = JLabel()
        self.jButton6 = JButton()
        self.jButton12 = JButton()
        self.jButton19 = JButton()
        self.jPanel8 = JPanel()
        self.jButton11 = JButton()
        self.jTextField1 = JTextField()
        self.jTextField23 = JTextField()
        self.jButton17 = JButton()
        self.jPanel1 = JPanel()
        self.jTextField2 = JTextField()
        self.jButton13 = JButton()
        self.jTextField3 = JTextField()
        self.jTextField4 = JTextField()
        self.jButton14 = JButton()
        self.jTextField5 = JTextField()
        self.jTextField6 = JTextField()
        self.jTextField7 = JTextField()
        self.jTextField8 = JTextField()
        self.jTextField9 = JTextField()
        self.jTextField10 = JTextField()
        self.jTextField11 = JTextField()
        self.jTextField12 = JTextField()
        self.jTextField13 = JTextField()
        self.jTextField14 = JTextField()
        self.jTextField15 = JTextField()
        self.jTextField16 = JTextField()
        self.jTextField17 = JTextField()
        self.jTextField18 = JTextField()
        self.jTextField19 = JTextField()
        self.jPanel2 = JPanel()
        self.jTextField20 = JTextField()
        self.jTextField21 = JTextField()
        self.jButton15 = JButton()
        self.jPanel3 = JPanel()
        self.jTextField24 = JTextField()
        self.jTextField25 = JTextField()
        self.jButton18 = JButton()
        self.jTextField26 = JTextField()
        self.checkbox1 = Checkbox()
        self.jButton20 = JButton()
        self.jButton21 = JButton()
        self.jTabbedPane1 = JTabbedPane()
        self.jLabel3 = JLabel()
        self.jLabel4 = JLabel()
        self.jLabel5 = JLabel()
        self.jLabel6 = JLabel()
        self.jLabel7 = JLabel()
        self.setDefaultCloseOperation(3)
        self.jScrollPane1.setViewportView(self.chatLog)
        self.jButton10.setText("启动服务端")
        self.jButton10.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton10ActionPerformed(evt)
        self.jTextField22.setText("关闭服务器倒数时间")
        self.jTextField22.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jTextField22ActionPerformed(evt)
        self.jButton16.setText("关闭服务器")
        self.jButton16.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton16ActionPerformed(evt)
        self.jButton22.setText("查询总计在线人数")
        self.jButton22.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton22ActionPerformed(evt)
        self.jButton23.setText("断开全服玩家")
        self.jButton23.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton23ActionPerformed(evt)
        self.jTextArea1.setColumns(20)
        self.jTextArea1.setRows(5)
        self.jTextArea1.setText("怀旧冒险岛079V6整合版本 ")
        self.jScrollPane2.setViewportView(self.jTextArea1)
        jPanel5Layout = GroupLayout(self.jPanel5)
        self.jPanel5.setLayout(jPanel5Layout)
        jPanel5Layout.setHorizontalGroup(jPanel5Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel5Layout.createSequentialGroup().addGap(23, 23, 23).addGroup(jPanel5Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel5Layout.createSequentialGroup().addComponent(self.jButton22, -2, 134, -2).addGap(18, 18, 18).addComponent(self.jTextField22, -2, -1, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, 26, 32767).addComponent(self.jButton23, -2, 134, -2)).addGroup(jPanel5Layout.createSequentialGroup().addGroup(jPanel5Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addComponent(self.jButton16, -2, 134, -2).addComponent(self.jButton10, -2, 134, -2)).addGap(18, 18, 18).addComponent(self.jScrollPane2))).addGap(24, 24, 24)))
        jPanel5Layout.setVerticalGroup(jPanel5Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel5Layout.createSequentialGroup().addContainerGap(-1, 32767).addGroup(jPanel5Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(GroupLayout.Alignment.TRAILING, jPanel5Layout.createSequentialGroup().addComponent(self.jButton10, -2, 49, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton16, -2, 49, -2)).addComponent(self.jScrollPane2, GroupLayout.Alignment.TRAILING, -2, -1, -2)).addGap(18, 18, 18).addGroup(jPanel5Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jButton22).addComponent(self.jTextField22, -2, -1, -2).addComponent(self.jButton23)).addGap(8, 8, 8)))
        self.jTabbedPane2.addTab("服务器配置", self.jPanel5)
        self.jButton7.setText("保存数据")
        self.jButton7.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton7ActionPerformed(evt)
        self.jButton8.setText("保存雇佣")
        self.jButton8.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton8ActionPerformed(evt)
        self.jLabel2.setText("保存系列：")
        jPanel7Layout = GroupLayout(self.jPanel7)
        self.jPanel7.setLayout(jPanel7Layout)
        jPanel7Layout.setHorizontalGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel7Layout.createSequentialGroup().addContainerGap().addGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addComponent(self.jLabel2).addGroup(jPanel7Layout.createSequentialGroup().addComponent(self.jButton7).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton8))).addContainerGap(295, 32767)))
        jPanel7Layout.setVerticalGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel7Layout.createSequentialGroup().addContainerGap().addComponent(self.jLabel2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(jPanel7Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jButton7).addComponent(self.jButton8)).addContainerGap(125, 32767)))
        self.jTabbedPane2.addTab("保存数据", self.jPanel7)
        self.jButton9.setText("重载任务")
        self.jButton9.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton9ActionPerformed(evt)
        self.jButton1.setText("重载副本")
        self.jButton1.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton1ActionPerformed(evt)
        self.jButton5.setText("重载爆率")
        self.jButton5.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton5ActionPerformed(evt)
        self.jButton4.setText("重载商店")
        self.jButton4.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton4ActionPerformed(evt)
        self.jButton3.setText("重载传送门")
        self.jButton3.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton3ActionPerformed(evt)
        self.jButton2.setText("重载反应堆")
        self.jButton2.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton2ActionPerformed(evt)
        self.jLabel1.setText("重载系列：")
        self.jButton6.setText("重载包头")
        self.jButton6.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton6ActionPerformed(evt)
        self.jButton12.setText("重载商城")
        self.jButton12.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton12ActionPerformed(evt)
        self.jButton19.setText("清除Sql連線")
        self.jButton19.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton19ActionPerformed(evt)
        jPanel6Layout = GroupLayout(self.jPanel6)
        self.jPanel6.setLayout(jPanel6Layout)
        jPanel6Layout.setHorizontalGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel6Layout.createSequentialGroup().addContainerGap().addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addComponent(self.jLabel1).addGroup(jPanel6Layout.createSequentialGroup().addComponent(self.jButton6).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton12)).addGroup(jPanel6Layout.createSequentialGroup().addComponent(self.jButton1).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton5).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton2).addGap(12, 12, 12).addComponent(self.jButton3)).addGroup(jPanel6Layout.createSequentialGroup().addComponent(self.jButton9).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton4)).addComponent(self.jButton19)).addContainerGap(91, 32767)))
        jPanel6Layout.setVerticalGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel6Layout.createSequentialGroup().addContainerGap().addComponent(self.jLabel1).addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jButton3).addComponent(self.jButton2)).addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jButton1).addComponent(self.jButton5))).addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED).addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jButton9).addComponent(self.jButton4)).addGap(10, 10, 10).addGroup(jPanel6Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jButton6).addComponent(self.jButton12)).addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED).addComponent(self.jButton19).addContainerGap(32, 32767)))
        self.jTabbedPane2.addTab("重载系列", self.jPanel6)
        self.jButton11.setText("解卡玩家")
        self.jButton11.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton11ActionPerformed(evt)
        self.jTextField1.setText("输入玩家名字")
        self.jTextField1.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jTextField1ActionPerformed(evt)
        self.jTextField23.setText("输入账号")
        self.jTextField23.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jTextField23ActionPerformed(evt)
        self.jButton17.setText("解卡账号")
        self.jButton17.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton17ActionPerformed(evt)
        jPanel8Layout = GroupLayout(self.jPanel8)
        self.jPanel8.setLayout(jPanel8Layout)
        jPanel8Layout.setHorizontalGroup(jPanel8Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel8Layout.createSequentialGroup().addContainerGap().addGroup(jPanel8Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel8Layout.createSequentialGroup().addComponent(self.jTextField1, -2, 124, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton11)).addGroup(jPanel8Layout.createSequentialGroup().addComponent(self.jTextField23, -2, 124, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton17))).addContainerGap(252, 32767)))
        jPanel8Layout.setVerticalGroup(jPanel8Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel8Layout.createSequentialGroup().addContainerGap().addGroup(jPanel8Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField1, -2, -1, -2).addComponent(self.jButton11)).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(jPanel8Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField23, -2, -1, -2).addComponent(self.jButton17)).addContainerGap(117, 32767)))
        self.jTabbedPane2.addTab("卡号处理", self.jPanel8)
        self.jTextField2.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jTextField2ActionPerformed(evt)
        self.jButton13.setText("公告发布")
        self.jButton13.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton13ActionPerformed(evt)
        self.jTextField3.setText("玩家名字")
        self.jTextField4.setText("物品ID")
        self.jButton14.setText("给予物品")
        self.jButton14.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton14ActionPerformed(evt)
        self.jTextField5.setText("数量")
        self.jTextField6.setText("力量")
        self.jTextField7.setText("敏捷")
        self.jTextField8.setText("智力")
        self.jTextField9.setText("运气")
        self.jTextField10.setText("HP设置")
        self.jTextField11.setText("MP设置")
        self.jTextField12.setText("加卷次数")
        self.jTextField13.setText("制作人")
        self.jTextField14.setText("给予物品时间")
        self.jTextField15.setText("可以交易")
        self.jTextField16.setText("攻击力")
        self.jTextField17.setText("魔法力")
        self.jTextField18.setText("物理防御")
        self.jTextField19.setText("魔法防御")
        jPanel1Layout = GroupLayout(self.jPanel1)
        self.jPanel1.setLayout(jPanel1Layout)
        jPanel1Layout.setHorizontalGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel1Layout.createSequentialGroup().addContainerGap().addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel1Layout.createSequentialGroup().addComponent(self.jTextField2, -1, 354, 32767).addGap(18, 18, 18).addComponent(self.jButton13)).addGroup(jPanel1Layout.createSequentialGroup().addComponent(self.jTextField3, -2, 92, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jTextField4, -2, 77, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jTextField5, -2, 52, -2)).addGroup(jPanel1Layout.createSequentialGroup().addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING, False).addGroup(jPanel1Layout.createSequentialGroup().addComponent(self.jTextField9, -2, 58, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jTextField13)).addGroup(GroupLayout.Alignment.TRAILING, jPanel1Layout.createSequentialGroup().addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.TRAILING).addComponent(self.jTextField8).addComponent(self.jTextField7)).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING, False).addComponent(self.jTextField11, -2, 79, -2).addComponent(self.jTextField12, -2, 79, -2))).addGroup(jPanel1Layout.createSequentialGroup().addComponent(self.jTextField6, -2, 58, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jTextField10, -2, 79, -2))).addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED).addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING, False).addComponent(self.jTextField16).addComponent(self.jTextField15).addComponent(self.jTextField14).addComponent(self.jTextField17)).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING, False).addComponent(self.jButton14, -1, -1, 32767).addComponent(self.jTextField18).addComponent(self.jTextField19)))).addContainerGap()))
        jPanel1Layout.setVerticalGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel1Layout.createSequentialGroup().addContainerGap().addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField2, -2, -1, -2).addComponent(self.jButton13)).addGap(18, 18, 18).addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField3, -2, -1, -2).addComponent(self.jTextField4, -2, -1, -2).addComponent(self.jTextField5, -2, -1, -2)).addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED).addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField6, -2, -1, -2).addComponent(self.jTextField10, -2, -1, -2).addComponent(self.jTextField14, -2, -1, -2).addComponent(self.jTextField18, -2, -1, -2)).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField7, -2, -1, -2).addComponent(self.jTextField11, -2, -1, -2).addComponent(self.jTextField15, -2, -1, -2).addComponent(self.jTextField19, -2, -1, -2)).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField8, -2, -1, -2).addComponent(self.jTextField12, -2, -1, -2).addComponent(self.jTextField16, -2, -1, -2)).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addGroup(jPanel1Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField9, -2, -1, -2).addComponent(self.jTextField13, -2, -1, -2).addComponent(self.jTextField17, -2, -1, -2).addComponent(self.jButton14)).addContainerGap(-1, 32767)))
        self.jTabbedPane2.addTab("指令/公告", self.jPanel1)
        self.jTextField20.setText("输入数量")
        self.jTextField20.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jTextField20ActionPerformed(evt)
        self.jTextField21.setText("1点卷/2抵用/3金币/4经验")
        self.jButton15.setText("发放全服点卷/抵用卷/金币/经验")
        self.jButton15.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton15ActionPerformed(evt)
        jPanel2Layout = GroupLayout(self.jPanel2)
        self.jPanel2.setLayout(jPanel2Layout)
        jPanel2Layout.setHorizontalGroup(jPanel2Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel2Layout.createSequentialGroup().addContainerGap().addComponent(self.jTextField20, -2, 88, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jTextField21, -2, -1, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jButton15).addContainerGap(-1, 32767)))
        jPanel2Layout.setVerticalGroup(jPanel2Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel2Layout.createSequentialGroup().addContainerGap().addGroup(jPanel2Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField20, -2, -1, -2).addComponent(self.jTextField21, -2, -1, -2).addComponent(self.jButton15)).addContainerGap(146, 32767)))
        self.jTabbedPane2.addTab("奖励系列", self.jPanel2)
        self.jTextField24.setText("账号")
        self.jTextField24.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jTextField24ActionPerformed(evt)
        self.jTextField25.setText("新密码")
        self.jTextField25.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jTextField25ActionPerformed(evt)
        self.jButton18.setText("修改密码")
        self.jButton18.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton18ActionPerformed(evt)
        self.jTextField26.setText("万能密码")
        self.jTextField26.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jTextField26ActionPerformed(evt)
        self.checkbox1.setCursor(Cursor(0))
        self.checkbox1.setName("123")
        self.checkbox1.addMouseListener(MouseAdapter()
            public void mouseClicked(final MouseEvent evt)
                HuaiMS.self.checkbox1MouseClicked(evt)
        self.jButton20.setText("设置可万能登录")
        self.jButton20.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton20ActionPerformed(evt)
        self.jButton21.setText("取消其万能登录权限")
        self.jButton21.addActionListener(ActionListener()
            public void actionPerformed(final ActionEvent evt)
                HuaiMS.self.jButton21ActionPerformed(evt)
        jPanel3Layout = GroupLayout(self.jPanel3)
        self.jPanel3.setLayout(jPanel3Layout)
        jPanel3Layout.setHorizontalGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel3Layout.createSequentialGroup().addContainerGap().addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel3Layout.createSequentialGroup().addComponent(self.jTextField24, -2, 88, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jTextField25, -2, 88, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.jTextField26, -2, 88, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED).addComponent(self.checkbox1, -2, -1, -2).addPreferredGap(LayoutStyle.ComponentPlacement.RELATED, -1, 32767).addComponent(self.jButton18).addGap(181, 181, 181)).addGroup(jPanel3Layout.createSequentialGroup().addComponent(self.jButton20).addGap(18, 18, 18).addComponent(self.jButton21).addContainerGap(-1, 32767)))))
        jPanel3Layout.setVerticalGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(jPanel3Layout.createSequentialGroup().addContainerGap().addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.TRAILING).addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jTextField24, -2, -1, -2).addComponent(self.jTextField25, -2, -1, -2).addComponent(self.jTextField26, -2, -1, -2).addComponent(self.jButton18)).addComponent(self.checkbox1, -2, -1, -2)).addGap(18, 18, 18).addGroup(jPanel3Layout.createParallelGroup(GroupLayout.Alignment.BASELINE).addComponent(self.jButton20).addComponent(self.jButton21)).addContainerGap(105, 32767)))
        self.jTabbedPane2.addTab("账号服务", self.jPanel3)
        self.jLabel3.setFont(Font("宋体", 1, 12))
        self.jLabel3.setText("   本程序来自互联网 仅供学习测试 禁止商业用途 否则本人不承担任何后果")
        self.jTabbedPane1.addTab("公告申明", self.jLabel3)
        self.jLabel4.setFont(Font("宋体", 1, 12))
        self.jLabel4.setText("       版本号：V079_MAX正式版")
        self.jTabbedPane1.addTab("版权说明", self.jLabel4)
        self.jLabel5.setFont(Font("宋体", 1, 12))
        self.jLabel5.setText("      修复大量BUG 修复全任务 全副本 全BOSS 全剧情完美 全职业完美 ")
        self.jTabbedPane1.addTab("更新内容A", self.jLabel5)
        self.jLabel6.setFont(Font("宋体", 1, 12))
        self.jLabel6.setText("      修复卡号    修复双登    修复复制     修复假死    修复掉线")
        self.jTabbedPane1.addTab("更新内容B", self.jLabel6)
        self.jLabel7.setFont(Font("宋体", 1, 12))
        self.jLabel7.setText("      修复多线程   修复炸线   增加全新的外挂检测   增加大量函数")
        self.jTabbedPane1.addTab("更新内容C", self.jLabel7)
        self.jTabbedPane2.addTab("关于我们", self.jTabbedPane1)
        layout = GroupLayout(self.getContentPane())
        self.getContentPane().setLayout(layout)
        layout.setHorizontalGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING).addComponent(self.jScrollPane1).addGroup(layout.createSequentialGroup().addContainerGap(478, 32767).addComponent(self.canvas1, -2, -1, -2)).addComponent(self.jTabbedPane2, -2, 0, 32767))
        layout.setVerticalGroup(layout.createParallelGroup(GroupLayout.Alignment.LEADING).addGroup(layout.createSequentialGroup().addComponent(self.jTabbedPane2).addGap(5, 5, 5).addComponent(self.canvas1, -2, -1, -2).addGap(20, 20, 20).addComponent(self.jScrollPane1, -2, 93, -2).addContainerGap()))
        self.pack()

    def actionPerformed(self, evt: Any) -> None:
        HuaiMS.self.jButton10ActionPerformed(evt)

    def actionPerformed_evt(self, evt: Any) -> None:
        HuaiMS.self.jTextField22ActionPerformed(evt)

    def mouseClicked(self, evt: Any) -> None:
        HuaiMS.self.checkbox1MouseClicked(evt)

    def jButton1ActionPerformed(self, evt: Any) -> None:
        for instance1 in ChannelServer.getAllInstances():
            if instance1 is not None:
                instance1.reloadEvents()
        输出 = "[重载系统] 副本重载成功。"
        JOptionPane.showMessageDialog(None, "副本重载成功。")
        self.printChatLog(输出)

    def jButton5ActionPerformed(self, evt: Any) -> None:
        MapleMonsterInformationProvider.getInstance().clearDrops()
        输出 = "[重载系统] 爆率重载成功。"
        JOptionPane.showMessageDialog(None, "爆率重载成功。")
        self.printChatLog(输出)

    def jButton6ActionPerformed(self, evt: Any) -> None:
        SendPacketOpcode.reloadValues()
        RecvPacketOpcode.reloadValues()
        输出 = "[重载系统] 包头重载成功。"
        JOptionPane.showMessageDialog(None, "包头重载成功。")
        self.printChatLog(输出)

    def jButton3ActionPerformed(self, evt: Any) -> None:
        PortalScriptManager.getInstance().clearScripts()
        输出 = "[重载系统] 传送门重载成功。"
        JOptionPane.showMessageDialog(None, "传送门重载成功。")
        self.printChatLog(输出)

    def jButton4ActionPerformed(self, evt: Any) -> None:
        MapleShopFactory.getInstance().clear()
        输出 = "[重载系统] 商店重载成功。"
        JOptionPane.showMessageDialog(None, "商店重载成功。")
        self.printChatLog(输出)

    def jButton2ActionPerformed(self, evt: Any) -> None:
        ReactorScriptManager.getInstance().clearDrops()
        输出 = "[重载系统] 反应堆重载成功。"
        JOptionPane.showMessageDialog(None, "反应堆重载成功。")
        self.printChatLog(输出)

    def jButton9ActionPerformed(self, evt: Any) -> None:
        MapleQuest.clearQuests()
        输出 = "[重载系统] 任务重载成功。"
        JOptionPane.showMessageDialog(None, "任务重载成功。")
        self.printChatLog(输出)

    def jButton8ActionPerformed(self, evt: Any) -> None:
        p = 0
        for cserv in ChannelServer.getAllInstances():
            p += 1
            cserv.closeAllMerchant()
        输出 = "[保存雇佣商人系统] 雇佣商人保存" + p + "个频道成功。"
        JOptionPane.showMessageDialog(None, "雇佣商人保存" + p + "个频道成功。")
        self.printChatLog(输出)

    def jButton7ActionPerformed(self, evt: Any) -> None:
        p = 0
        for cserv in ChannelServer.getAllInstances():
            for chr in cserv.getPlayerStorage().getAllCharacters():
                p += 1
                chr.saveToDB(True, True)
        输出 = "[保存数据系统] 保存" + p + "个成功。"
        JOptionPane.showMessageDialog(None, 输出)
        self.printChatLog(输出)

    def jButton10ActionPerformed(self, evt: Any) -> None:
        try:
            if Start.Check:
                Start.instance.startServer()
                输出 = "[服务器] 服务器启动成功！"
                self.printChatLog(输出)
            else:
                JOptionPane.showMessageDialog(None, "[服务器] 无法重复运行。")
        except InterruptedException as ex:
            Logger.getLogger(HuaiMS.class.getName()).log(Level.SEVERE, None, ex)

    def jTextField1ActionPerformed(self, evt: Any) -> None:
        pass

    def jButton11ActionPerformed(self, evt: Any) -> None:
        self.sendNotice(0)

    def jButton12ActionPerformed(self, evt: Any) -> None:
        CashItemFactory.getInstance().clearCashShop()
        输出 = "[重载系统] 商城重载成功。"
        JOptionPane.showMessageDialog(None, "商城重载成功。")
        self.printChatLog(输出)

    def jTextField2ActionPerformed(self, evt: Any) -> None:
        pass

    def jButton13ActionPerformed(self, evt: Any) -> None:
        self.sendNoticeGG()

    def jButton14ActionPerformed(self, evt: Any) -> None:
        self.刷物品()

    def jTextField20ActionPerformed(self, evt: Any) -> None:
        pass

    def jButton15ActionPerformed(self, evt: Any) -> None:
        self.给全服点卷()

    def jButton16ActionPerformed(self, evt: Any) -> None:
        self.重启服务器()

    def jTextField22ActionPerformed(self, evt: Any) -> None:
        pass

    def jTextField23ActionPerformed(self, evt: Any) -> None:
        pass

    def jButton17ActionPerformed(self, evt: Any) -> None:
        self.FixAcLogged()

    def jTextField24ActionPerformed(self, evt: Any) -> None:
        pass

    def jTextField25ActionPerformed(self, evt: Any) -> None:
        pass

    def jButton18ActionPerformed(self, evt: Any) -> None:
        self.ChangePassWord()

    def jButton19ActionPerformed(self, evt: Any) -> None:
        DatabaseConnection.closeTimeout()

    def jTextField26ActionPerformed(self, evt: Any) -> None:
        pass

    def checkbox1MouseClicked(self, evt: Any) -> None:
        status = self.checkbox1.getState()
        if !(ServerConstants.Super_password = status):
            ServerConstants.superpw = ""
        else:
            ServerConstants.superpw = self.jTextField26.getText()

    def jButton20ActionPerformed(self, evt: Any) -> None:
        self.可以万能登录()

    def jButton21ActionPerformed(self, evt: Any) -> None:
        self.不可以万能登录()

    def jButton22ActionPerformed(self, evt: Any) -> None:
        p = 0
        for cserv in ChannelServer.getAllInstances():
            for chr in cserv.getPlayerStorage().getAllCharacters():
                if chr is not None:
                    p += 1
        JOptionPane.showMessageDialog(this, "当前在线人数：" + p + "人")

    def jButton23ActionPerformed(self, evt: Any) -> None:
        for cserv in ChannelServer.getAllInstances():
            cserv.getPlayerStorage().disconnectAll(True)
        JOptionPane.showMessageDialog(None, "已断开全部频道玩家")

    def translated_不可以万能登录(self) -> None:
        account = self.jTextField24.getText()
        if !AutoRegister.getAccountExists(account):
            JOptionPane.showMessageDialog(None, "账号不存在")
            return
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("Update accounts set handsome = ? Where name = ?")
            ps.setString(1, "1")
            ps.setString(2, account)
            ps.execute()
            ps.close()
        except Exception as ex:
            JOptionPane.showMessageDialog(None, "错误!\r\n" + ex)
        JOptionPane.showMessageDialog(None, "成功取消其万能权限")
        self.printChatLog("更改账号: " + account + " .设置取消其万能登录权限。")

    def translated_可以万能登录(self) -> None:
        account = self.jTextField24.getText()
        if !AutoRegister.getAccountExists(account):
            JOptionPane.showMessageDialog(None, "账号不存在")
            return
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("Update accounts set handsome = ? Where name = ?")
            ps.setString(1, "0")
            ps.setString(2, account)
            ps.execute()
            ps.close()
        except Exception as ex:
            JOptionPane.showMessageDialog(None, "错误!\r\n" + ex)
        JOptionPane.showMessageDialog(None, "成功设置万能登录权限")
        self.printChatLog("更改账号: " + account + " .设置其可以万能登录游戏.")

    def ChangePassWord(self) -> None:
        account = self.jTextField24.getText()
        password = self.jTextField25.getText()
        if password > 12:
            JOptionPane.showMessageDialog(None, "密码过长")
            return
        if !AutoRegister.getAccountExists(account):
            JOptionPane.showMessageDialog(None, "账号不存在")
            return
        try:
            con = DatabaseConnection.getConnection()
            ps = con.prepareStatement("Update accounts set password = ? Where name = ?")
            ps.setString(1, LoginCrypto.hexSha1(password))
            ps.setString(2, account)
            ps.execute()
            ps.close()
        except Exception as ex:
            JOptionPane.showMessageDialog(None, "错误!\r\n" + ex)
        self.printChatLog("更改账号: " + account + "的密码为 " + password)

    def translated_重启服务器(self) -> None:
        try:
            输出 = "关闭服务器倒数时间"
            self.minutesLeft = int(self.jTextField22.getText())
            if HuaiMS.ts is None && (HuaiMS.t is None || !HuaiMS.t.isAlive()):
                HuaiMS.t = Thread(ShutdownServer.getInstance())
                HuaiMS.ts = Timer.EventTimer.getInstance().register(Runnable()
                    public void run()
                        if HuaiMS.self.minutesLeft == 0:
                            ShutdownServer.getInstance()
                            HuaiMS.t.start()
                            HuaiMS.ts.cancel(False)
                            return
                        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(0, "服务器將在 " + HuaiMS.self.minutesLeft + "分钟后关闭. 请尽快关闭雇佣商人安全下线.").encode("utf-8"))
                        print("服务器將在 " + HuaiMS.self.minutesLeft + "分钟后关闭.")
                        HuaiMS.self.minutesLeft -= 1
            self.jTextField22.setText("关闭服务器倒数时间")
            self.printChatLog(输出)
        except Exception as e:
            JOptionPane.showMessageDialog(None, "错误!\r\n" + e)

    def run(self) -> None:
        if HuaiMS.self.minutesLeft == 0:
            ShutdownServer.getInstance()
            HuaiMS.t.start()
            HuaiMS.ts.cancel(False)
            return
        World.Broadcast.broadcastMessage(MaplePacketCreator.serverNotice(0, "服务器將在 " + HuaiMS.self.minutesLeft + "分钟后关闭. 请尽快关闭雇佣商人安全下线.").encode("utf-8"))
        print("服务器將在 " + HuaiMS.self.minutesLeft + "分钟后关闭.")
        HuaiMS.self.minutesLeft -= 1

    def translated_给全服点卷(self) -> None:
        try:
            数量 = None
            if "输入数量" == (self.jTextField20.getText()):
                数量 = 0
            else:
                数量 = int(self.jTextField20.getText())
            类型 = None
            if "1点卷/2抵用/3金币/4经验" == (self.jTextField21.getText()):
                类型 = 0
            else:
                类型 = int(self.jTextField21.getText())
            if 数量 <= 0 || 类型 <= 0:
                return
            输出 = ""
            ret = 0
            if 类型 == 1 || 类型 == 2:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.modifyCSPoints(类型, 数量)
                        cash = None
                        if 类型 == 1:
                            cash = "点卷"
                        elif 类型 == 2:
                            cash = "抵用卷"
                        mch.startMapEffect("管理员发放" + 数量 + cash + "给在线的所有玩家！快感谢管理员吧！", 5121009)
                        ret += 1
            elif 类型 == 3:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.gainMeso(数量, True)
                        mch.startMapEffect("管理员发放" + 数量 + "冒险币给在线的所有玩家！快感谢管理员吧！", 5121009)
                        ret += 1
            elif 类型 == 4:
                for cserv1 in ChannelServer.getAllInstances():
                    for mch in cserv1.getPlayerStorage().getAllCharacters():
                        mch.gainExp(数量, True, False, True)
                        mch.startMapEffect("管理员发放" + 数量 + "经验给在线的所有玩家！快感谢管理员吧！", 5121009)
                        ret += 1
            类型A = ""
            if 类型 == 1:
                类型A = "点卷"
            elif 类型 == 2:
                类型A = "抵用卷"
            elif 类型 == 3:
                类型A = "金币"
            elif 类型 == 4:
                类型A = "经验"
            输出 = "一个发放[" + 数量 * ret + "]." + 类型A + "!一共发放给了" + ret + "人！"
            self.jTextField20.setText("输入数量")
            self.jTextField21.setText("1点卷/2抵用/3金币/4经验")
            self.printChatLog(输出)
        except Exception as e:
            JOptionPane.showMessageDialog(None, "错误!\r\n" + e)

    def translated_刷物品(self) -> None:
        try:
            名字 = None
            if "玩家名字" == (self.jTextField3.getText()):
                名字 = ""
            else:
                名字 = self.jTextField3.getText()
            物品ID = None
            if "物品ID" == (self.jTextField4.getText()):
                物品ID = 0
            else:
                物品ID = int(self.jTextField4.getText())
            数量 = None
            if "数量" == (self.jTextField5.getText()):
                数量 = 0
            else:
                数量 = int(self.jTextField5.getText())
            力量 = None
            if "力量" == (self.jTextField6.getText()):
                力量 = 0
            else:
                力量 = int(self.jTextField6.getText())
            敏捷 = None
            if "敏捷" == (self.jTextField7.getText()):
                敏捷 = 0
            else:
                敏捷 = int(self.jTextField7.getText())
            智力 = None
            if "智力" == (self.jTextField8.getText()):
                智力 = 0
            else:
                智力 = int(self.jTextField8.getText())
            运气 = None
            if "运气" == (self.jTextField9.getText()):
                运气 = 0
            else:
                运气 = int(self.jTextField9.getText())
            HP = None
            if "HP设置" == (self.jTextField10.getText()):
                HP = 0
            else:
                HP = int(self.jTextField10.getText())
            MP = None
            if "MP设置" == (self.jTextField11.getText()):
                MP = 0
            else:
                MP = int(self.jTextField11.getText())
            可加卷次数 = None
            if "加卷次数" == (self.jTextField12.getText()):
                可加卷次数 = 0
            else:
                可加卷次数 = int(self.jTextField12.getText())
            制作人名字 = None
            if "制作人" == (self.jTextField13.getText()):
                制作人名字 = ""
            else:
                制作人名字 = self.jTextField13.getText()
            给予时间 = None
            if "给予物品时间" == (self.jTextField14.getText()):
                给予时间 = 0
            else:
                给予时间 = int(self.jTextField14.getText())
            是否可以交易 = self.jTextField15.getText()
            攻击力 = None
            if "攻击力" == (self.jTextField16.getText()):
                攻击力 = 0
            else:
                攻击力 = int(self.jTextField16.getText())
            魔法力 = None
            if "魔法力" == (self.jTextField17.getText()):
                魔法力 = 0
            else:
                魔法力 = int(self.jTextField17.getText())
            物理防御 = None
            if "物理防御" == (self.jTextField18.getText()):
                物理防御 = 0
            else:
                物理防御 = int(self.jTextField18.getText())
            魔法防御 = None
            if "魔法防御" == (self.jTextField19.getText()):
                魔法防御 = 0
            else:
                魔法防御 = int(self.jTextField19.getText())
            ii = MapleItemInformationProvider.getInstance()
            type = GameConstants.getInventoryType(物品ID)
            输出A = ""
            输出 = "玩家名字：" + 名字 + " 物品ID：" + 物品ID + " 数量：" + 数量 + " 力量:" + 力量 + " 敏捷:" + 敏捷 + " 智力:" + 智力 + " 运气:" + 运气 + " HP:" + HP + " MP:" + MP + " 可加卷次数:" + 可加卷次数 + " 制作人名字:" + 制作人名字 + " 给予时间:" + 给予时间 + " 是否可以交易:" + 是否可以交易 + " 攻击力:" + 攻击力 + " 魔法力:" + 魔法力 + " 物理防御:" + 物理防御 + " 魔法防御:" + 魔法防御 + "\r\n"
            for cserv1 in ChannelServer.getAllInstances():
                for mch in cserv1.getPlayerStorage().getAllCharacters():
                    if mch.getName() == (名字):
                        if 数量 >= 0:
                            if !MapleInventoryManipulator.checkSpace(mch.getClient(), 物品ID, 数量, ""):
                                return
                            if (type == (MapleInventoryType.EQUIP) && !GameConstants.isThrowingStar(物品ID) && !GameConstants.isBullet(物品ID)) || (type == (MapleInventoryType.CASH) && 物品ID >= 5000000 && 物品ID <= 5000100):
                                item = ii.getEquipById(物品ID)
                                if ii.isCash(物品ID):
                                    item.setUniqueId(1)
                                if 力量 > 0 && 力量 <= 32767:
                                    item.setStr(力量)
                                if 敏捷 > 0 && 敏捷 <= 32767:
                                    item.setDex(敏捷)
                                if 智力 > 0 && 智力 <= 32767:
                                    item.setInt(智力)
                                if 运气 > 0 && 运气 <= 32767:
                                    item.setLuk(运气)
                                if 攻击力 > 0 && 攻击力 <= 32767:
                                    item.setWatk(攻击力)
                                if 魔法力 > 0 && 魔法力 <= 32767:
                                    item.setMatk(魔法力)
                                if 物理防御 > 0 && 物理防御 <= 32767:
                                    item.setWdef(物理防御)
                                if 魔法防御 > 0 && 魔法防御 <= 32767:
                                    item.setMdef(魔法防御)
                                if HP > 0 && HP <= 30000:
                                    item.setHp(HP)
                                if MP > 0 && MP <= 30000:
                                    item.setMp(MP)
                                if "可以交易" == (是否可以交易):
                                    flag = item.getFlag()
                                    if item.getType() == MapleInventoryType.EQUIP.getType():
                                        flag |= ItemFlag.KARMA_EQ.getValue()
                                    else:
                                        flag |= ItemFlag.KARMA_USE.getValue()
                                    item.setFlag(flag)
                                if 给予时间 > 0:
                                    item.setExpiration(int(time.time() * 1000) + 给予时间 * 24 * 60 * 60 * 1000)
                                if 可加卷次数 > 0:
                                    item.setUpgradeSlots(可加卷次数)
                                if 制作人名字 is not None:
                                    item.setOwner(制作人名字)
                                name = ii.getName(物品ID)
                                if 物品ID / 10000 == 114 && name is not None && name > 0:
                                    msg = "你已获得称号 <" + name + ">"
                                    mch.getClient().getPlayer().dropMessage(5, msg)
                                    mch.getClient().getPlayer().dropMessage(5, msg)
                                MapleInventoryManipulator.addbyItem(mch.getClient(), item.copy())
                            else:
                                MapleInventoryManipulator.addById(mch.getClient(), 物品ID, 数量, "", None, 给予时间, 0)
                        else:
                            MapleInventoryManipulator.removeById(mch.getClient(), GameConstants.getInventoryType(物品ID), 物品ID, -数量, True, False)
                        mch.getClient().getSession().write(MaplePacketCreator.getShowItemGain(物品ID, 数量, True))
                        输出A = "[刷物品]:" + 输出
            self.jTextField3.setText("玩家名字")
            self.jTextField4.setText("物品ID")
            self.jTextField5.setText("数量")
            self.jTextField6.setText("力量")
            self.jTextField7.setText("敏捷")
            self.jTextField8.setText("智力")
            self.jTextField9.setText("运气")
            self.jTextField10.setText("HP设置")
            self.jTextField11.setText("MP设置")
            self.jTextField12.setText("加卷次数")
            self.jTextField13.setText("制作人")
            self.jTextField14.setText("给予物品时间")
            self.jTextField15.setText("可以交易")
            self.jTextField16.setText("攻击力")
            self.jTextField17.setText("魔法力")
            self.jTextField18.setText("物理防御")
            self.jTextField19.setText("魔法防御")
            self.printChatLog(输出A)
        except Exception as e:
            JOptionPane.showMessageDialog(None, "错误!\r\n" + e)

    def printChatLog(self, str: str) -> None:
        self.chatLog.setText(self.chatLog.getText() + str + "\r\n")

    def sendNoticeGG(self) -> None:
        try:
            str = self.jTextField2.getText()
            输出 = ""
            for cserv1 in ChannelServer.getAllInstances():
                for mch in cserv1.getPlayerStorage().getAllCharacters():
                    mch.startMapEffect(str, 5121009)
                    输出 = "[公告]:" + str
            self.jTextField2.setText("")
            self.printChatLog(输出)
        except Exception as e:
            JOptionPane.showMessageDialog(None, "错误!\r\n" + e)

    def FixAcLogged(self) -> None:
        try:
            final com.mysql.jdbc.Connection dcon = (com.mysql.jdbc.Connection)DatabaseConnection.getConnection()
            # try-with-resources: final com.mysql.jdbc.PreparedStatement ps = (com.mysql.jdbc.PreparedStatement)dcon.prepareStatement("UPDATE accounts SET loggedin = 0 WHERE name = " + self.jTextField23.getText())
            try:
                ps.executeUpdate()
            self.printChatLog("解除卡账号" + self.jTextField23.getText())
            self.jTextField23.setText("")
        catch (SQLException ex) {}

    def sendNotice(self, type: int) -> None:
        try:
            str = self.jTextField1.getText()
            p = None
            输出 = ""
            if type == 0:
                for cserv in ChannelServer.getAllInstances():
                    for chr in cserv.getPlayerStorage().getAllCharacters():
                        try:
                            ChannelServer.forceRemovePlayerByCharName(str)
                            if chr.getName() == (str) && chr.getMapId() != 0:
                                chr.getClient().getSession().close(True)
                                chr.getClient().disconnect(True, False)
                                输出 = "[解卡系统] 成功断开" + str + "玩家！"
                            else:
                                输出 = "[解卡系统] 玩家名字输入错误或者该玩家没有在线！"
                        catch (Exception ex) {}
            self.jTextField1.setText("")
            self.printChatLog(输出)
        except Exception as e:
            JOptionPane.showMessageDialog(None, "错误!\r\n" + e)

    def main(self, args: list) -> None:
        try:
            for (final UIManager.LookAndFeelInfo info : UIManager.getInstalledLookAndFeels())
                if "Nimbus" == (info.getName()):
                    UIManager.setLookAndFeel(info.getClassName())
                    break
        except ClassNotFoundException as ex:
            Logger.getLogger(HuaiMS.class.getName()).log(Level.SEVERE, None, ex)
        except InstantiationException as ex2:
            Logger.getLogger(HuaiMS.class.getName()).log(Level.SEVERE, None, ex2)
        except IllegalAccessException as ex3:
            Logger.getLogger(HuaiMS.class.getName()).log(Level.SEVERE, None, ex3)
        except UnsupportedLookAndFeelException as ex4:
            Logger.getLogger(HuaiMS.class.getName()).log(Level.SEVERE, None, ex4)
        EventQueue.invokeLater(Runnable()
            public void run()
                HuaiMS().setVisible(True)

