# chatroom
基于Django和Vue实现的建议网站，主要包含三部分：
- 1、基于websocket实现的多人在线聊天室；
- 2、实现一套相对比较完善的审批流功能模块；
- 3、实现一个基于elasticsearch搜索的查询模块

Vue组件库：vuetify

## 聊天室 chatroom
基于websocket实现的多人在线聊天室。

后端基于 Django channels 模块

## 审批流 approval
目标：实现每个节点可配置的工作流

难点：1、实现逻辑（审批结点设计、配置逻辑、流转逻辑）；2、数据库表设计

进度：待开发

## 搜索模块 search

进度：已完成

介绍：基于elasticsearch实现大数据关键字搜索，同时实现搜索匹配建议
