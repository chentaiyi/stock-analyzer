# Stock Analyzer

此项目为加密货币监控项目的A股精简版。
主要功能包括通过A股数据，实时分析监控A股行情，可自行配置监控标的品种，数量和技术分析信号及周期窗口，
可主动扫描符合信号的标的，也可实时监控符合条件时自动通过邮箱通知进行操作。

## 功能特点

##### 支持实时数据和历史数据的分析。
##### 支持自定义指标，根据自定义指标生成交易信号。
##### 支持主动扫描
##### 支持通过邮件进行交易信号的通知。
##### 自带macd halftrend、 smart money concepts(聪明钱)、nmacd、sslchannel等实用指标


## 环境要求

Python 3.6 及以上版本。
需要安装 pandas、numpy、tushare、matplotlib 和 smtplib 等第三方库。
安装命令：
pip install -r requestment.txt

## 使用说明

### 1.主要模块

##### 数据源使用Ashare封装，可更换其他数据源封装包。

##### 其中Indicator模块为相

##### Analysis模块为技术分析模块 对复杂的技术指标 ，ma、rsi等talib自带指标直接写在trading_signal

##### trading_signals为交易信号，交易信号可以是单指标或者指标组合。

##### Notifiers模块为通知模块，目前仅支持邮件，可以方便扩展到webhook 推特 discord等

##### exchange：获取交易数据 config：配置

### 2.配置config.json文件

##### pairlists：股票标的，支持Ashare两种格式'sh000001'或者'000001.XSHG'

##### signals：交易信号

##### scan：实际参与搜索和监控的信号

##### notifier:配置邮箱参数
包括发件人邮箱、SMTP 服务器地址、SMTP 端口号、发件人邮箱用户名和密码等。
其中发送邮箱的密码通常为应用专用密码，通常需进入邮箱服务器申请

##### 运行 main.py 

## 如何贡献

如果您发现了 Bug 或有任何改进建议，请在 Issues 中提出。
如果您愿意为该项目的开发和维护做出贡献，请 Fork 本项目，并提交 Pull Request。

## 作者

作者：chentaiyi
邮箱：501745@qq.com


