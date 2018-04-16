-- phpMyAdmin SQL Dump
-- version 4.6.5.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 26, 2018 at 07:00 PM
-- Server version: 10.1.21-MariaDB
-- PHP Version: 7.1.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `qc`
--

-- --------------------------------------------------------

--
-- Table structure for table `acct_mgmt`
--

CREATE TABLE `acct_mgmt` (
  `id` int(11) NOT NULL,
  `username` varchar(50) DEFAULT NULL,
  `pwd` varchar(50) DEFAULT NULL,
  `note` text,
  `authority` int(1) NOT NULL DEFAULT '1',
  `is_using` int(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;

--
-- Dumping data for table `acct_mgmt`
--

INSERT INTO `acct_mgmt` (`id`, `username`, `pwd`, `note`, `authority`, `is_using`) VALUES
(1, 'admin', 'admin', '管理员账户，顶级权限', 1, 1),
(2, 'avawang', 'avawang', 'QC Manager', 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `attachment`
--

CREATE TABLE `attachment` (
  `id` int(15) NOT NULL,
  `name` varchar(200) DEFAULT NULL,
  `date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `user` varchar(150) DEFAULT NULL,
  `qc_num` varchar(150) DEFAULT NULL,
  `status` int(2) NOT NULL DEFAULT '1',
  `comment` text,
  `url` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `attachment`
--

INSERT INTO `attachment` (`id`, `name`, `date`, `user`, `qc_num`, `status`, `comment`, `url`) VALUES
(3, '投诉附件', '2018-02-21 16:07:37', 'admin', '20180105', 1, '投诉附件投诉附件投诉附件投诉附件投诉附件投诉附件\r\n投诉附件投诉附件投诉附件投诉附件投诉附件投诉附件', 'https://netorg3585165-my.sharepoint.com/:i:/g/personal/kangyuwang_uvbookings_com/EYVNh9ZRqVFBltyB_ealrIwB3riGt-WeSUdqSu--aUggnQ?e=jtFbPY'),
(4, '321', '2018-02-22 17:36:19', 'admin', '20180105', 1, '312313', '123'),
(5, '大妈', '2018-02-23 16:49:52', 'avawang', '122717-1', 1, '大妈的小学照片', 'https://netorg3585165-my.sharepoint.com/:i:/g/personal/kangyuwang_uvbookings_com/EYVNh9ZRqVFBltyB_ealrIwB3riGt-WeSUdqSu--aUggnQ?e=2c7os5');

-- --------------------------------------------------------

--
-- Table structure for table `basic_info`
--

CREATE TABLE `basic_info` (
  `id` int(10) NOT NULL,
  `qc_num` varchar(20) DEFAULT NULL,
  `source` varchar(150) DEFAULT NULL,
  `source_subject` text,
  `status` varchar(50) DEFAULT NULL,
  `content` text,
  `ivsg_result` text,
  `creat_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `creator` varchar(30) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `basic_info`
--

INSERT INTO `basic_info` (`id`, `qc_num`, `source`, `source_subject`, `status`, `content`, `ivsg_result`, `creat_date`, `creator`) VALUES
(1, '#123#321', 'I am source', NULL, 'new', 'I am content', 'I am ivsg_result', '2017-12-26 18:39:29', 'test creator'),
(10, '20180105', 'phone_a', '', 'w_email', '我是投诉内容', '我是调查结果', '2018-01-05 18:28:00', 'admin'),
(11, '011818-8', 'email_a', '专业的旅游公司准许“带病”车辆运行/刘宝清 <liubaoqing@yeah.net>\r\n\r\n美东同事发微信\r\n回复:纵横集团品质管理部\r\n刘宝清 <liubaoqing@yeah.net>\r\n', 'new', '尊敬的纵横集团品质部领导好：\r\n由于12月30日和31日两天酒店都不能提供稳定的上网条件，1月1日晚上又限于时间短暂只是回复了你们“带病”车辆函件。故没有及时回复接站问题沟通邮件致歉。我将在我的旅程结束后需要一些时间来整理我掌握的你们26日没有接机的影像和音像资料，向你们还原当时现场事实。证明你们接机人的失职，证明你们品质部在处理我投诉的两个问题上所表现出来的傲慢和不作为。\r\n1、请提供你们集团总经理或董事长邮箱，我将向他们揭示他们领导下的接机员工是如何完成接机工作的？品质部是如何“重视”和处理客户合理投诉的？\r\n2、请提供你们集团董事局秘书处邮箱。我将向你们集团董事局质询：你们集团的“客户满意保障方案”，就是故意掩盖事实、无情侵害客户的基本权益的方案吗？', '微信导游：\r\ndispatcher 10:26 的时候在QQ 群跟美东报备 说客人还没找到。 接他们的导游是要带大巴的带车导游。 所以导游9 点左右没有找到客人，经leader 要求，就去别的航站楼帮忙接别的客人，然后带大巴去法拉盛了。一般我们在联系不上客人，找不到也报备公司的情况下，同时机场还有别的客人要接，没可能一直干等他们，只能等客人联系我们。 所以10 点多客人联系导游，才又安排了别的导游过去接他们（导游之所以没有当下马上接到他们而是11:30 左右接到，因为他联系我们的时候，导游正在接别的客人，接到安置好才跑过去接的ur1。 \r\n\\\\fs4\\2017\\14_QCD\\1. 投诉记录\\辅助材料\\122717#7', '2018-02-19 20:58:50', 'admin'),
(12, '122717-1', 'wechat', 'Complain about 12/26 WP1 /INV# JL003796\r\nlinling@57us.com', 'report', 'Dear，\r\n该订单出行人数为3个人，请核实，谢谢！\r\n\r\nDear Sir/Madam,\r\n现接到客人关于12/26 WP1 /INV# JL003796 行程投诉：\r\n明明是5美金的小费，司机却收了8美金，表示很不满意；\r\n而且贵司已经出现了不止一次这样的情况了，严重影响了我司的销售，麻烦退还客人8美金的全部小费，谢谢！\r\n盼复！', '我们没有强制性收小费的情况，因为其它部分平台的建议小费$8，这一家代理标明$5的话，客人应该当时就提出异议。希望该公司将小费标准改为$8。此次是否及退还标准，按贵公司原则处理吧。', '2018-02-23 21:43:34', 'avawang');

-- --------------------------------------------------------

--
-- Table structure for table `label_info`
--

CREATE TABLE `label_info` (
  `id` int(10) NOT NULL,
  `qc_num` varchar(20) DEFAULT NULL,
  `parent_title` varchar(100) DEFAULT NULL,
  `title` varchar(100) DEFAULT NULL,
  `memo` text,
  `label_num` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `label_info`
--

INSERT INTO `label_info` (`id`, `qc_num`, `parent_title`, `title`, `memo`, `label_num`) VALUES
(3, '20180105', 'title01', '我是子', NULL, NULL),
(4, '011818-8', '0', '我是标签', NULL, NULL),
(5, '011818-8', 'title01', '我是子', NULL, NULL),
(6, '122717-1', '0', '投诉部', NULL, NULL),
(7, '122717-1', '酒店部', '酒店部子标签', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `label_mgmt`
--

CREATE TABLE `label_mgmt` (
  `id` int(10) NOT NULL,
  `label_num` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `title` varchar(100) DEFAULT NULL,
  `level` int(1) NOT NULL DEFAULT '0',
  `parent` varchar(100) NOT NULL,
  `under` varchar(100) DEFAULT NULL,
  `comments` text,
  `comments_eng` text,
  `is_using` int(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `label_mgmt`
--

INSERT INTO `label_mgmt` (`id`, `label_num`, `title`, `level`, `parent`, `under`, `comments`, `comments_eng`, `is_using`) VALUES
(3, '2017-12-14 22:35:19', 'test010', 1, '0', 'NULL', 'comments lalalala 111', NULL, 1),
(4, '2017-12-20 19:42:28', 'Title1', 2, 'test', NULL, 'Test level 2', NULL, 1),
(5, '2017-12-21 17:32:11', 'title01', 1, '0', NULL, 'Test parent', NULL, 1),
(9, '2017-12-21 18:32:22', '我是标签', 1, '0', NULL, '跟代理解释酒店住在新泽西： \n最主要的是在纽约活动，酒店在纽约旁边的新泽西州纽瓦特，车程2个小时\n答：确实我们的酒店都是住在新泽西Edison到Newark区域之间，我们非常理解客人的抱怨，我们也是尽量减少客人的旅途疲劳，今年把我们的大多数酒店都是安排在Newark区域，Newark离曼哈顿是只有10几英里的距离，如果不塞车只需要15分钟就可以到达。但是问题是纽约的交通状况非常糟糕，特别是从曼哈顿到新泽西，我们今年也发生好几次，在隧道里塞车超过一个多小时。目前我们的美东产品由于团费和预算，只能住在新泽西，从体验来说确实是短期内很难解决的一个痛点', '酒店离餐厅太远：\nAccording to our investigation, we are aware that there was just 5-minute walk from the restaurant to hotel. That was not the highway. Also, the tour guide tried to give all the tourists more time to enjoy their dinner. There were many tourists wanted to buy something for next day. Therefore, the tour guide was waiting in front of the restaurant door and showed the tourists the direction to go to the supermarket and how to go back to hotel. Feedback towards tour guide\'s service was positive. Still, we will enhance our regulation on improvement of customer service in future days.\nenhance our regulation on improvement of customer service in future days.', 1),
(10, '2017-12-21 18:32:55', '我是子', 2, 'title01', NULL, '跟代理解释酒店住在新泽西： \n最主要的是在纽约活动，酒店在纽约旁边的新泽西州纽瓦特，车程2个小时\n答：确实我们的酒店都是住在新泽西Edison到Newark区域之间，我们非常理解客人的抱怨，我们也是尽量减少客人的旅途疲劳，今年把我们的大多数酒店都是安排在Newark区域，Newark离曼哈顿是只有10几英里的距离，如果不塞车只需要15分钟就可以到达。但是问题是纽约的交通状况非常糟糕，特别是从曼哈顿到新泽西，我们今年也发生好几次，在隧道里塞车超过一个多小时。目前我们的美东产品由于团费和预算，只能住在新泽西，从体验来说确实是短期内很难解决的一个痛点', '酒店离餐厅太远：\nAccording to our investigation, we are aware that there was just 5-minute walk from the restaurant to hotel. That was not the highway. Also, the tour guide tried to give all the tourists more time to enjoy their dinner. There were many tourists wanted to buy something for next day. Therefore, the tour guide was waiting in front of the restaurant door and showed the tourists the direction to go to the supermarket and how to go back to hotel. Feedback towards tour guide\'s service was positive. Still, we will enhance our regulation on improvement of customer service in future days.', 1),
(11, '2017-12-22 20:55:17', '我是表情', 1, '0', NULL, '你是标签吗', NULL, 1),
(12, '2018-02-05 22:20:11', '巴士部', 1, '0', NULL, '我是巴士部', NULL, 1),
(13, '2018-02-05 22:26:06', 'test1111111', 2, '巴士部', 'Title1', '水电费水电费沙发1', NULL, 1),
(14, '2018-02-05 22:27:04', '哈哈哈哈', 1, '0', NULL, '嘻嘻嘻嘻', NULL, 1),
(15, '2018-02-21 16:23:47', '酒店部', 1, '0', NULL, '空', '空', 1),
(16, '2018-02-21 16:24:47', '酒店部子标签', 2, '酒店部', 'NULL', '我是中文回复', '我是英文回复', 1),
(17, '2018-02-23 21:38:51', '投诉部', 1, '0', NULL, '对于此次订团操作出现的问题，我们深表歉意。作为一家团务操作者，我们绝对不会放弃履行我司应尽的责任。因此事造成的经济损失，我们愿意作出 $ #### 的赔偿。如有任何问题，请随时与我们取得联系，我们愿意全力协助解决此事。(如涉及职能部门的操作问题，可参考相应赔偿编号作出赔偿明晰)', 'Regarding any issues of this order, please accept our sincere apology. As a tour operator, we would never waive our responsibility on tour operations. For any extra financial expenditure occured, we hereby would like to make a compensation of $ ####. Please feel free to contact us if there is anything we could help with to settle this case down. (如涉及职能部门的操作问题，可参考相应赔偿编号作出赔偿明晰)', 1),
(18, '2018-02-23 21:39:42', '大妈抽烟', 2, '投诉部', 'NULL', '退团费范例:\r\n总团费: $890 \r\n酒店费用: $100/天*5天=$500\r\n巴士费用: $15/天每人*6天*1人 = $90\r\n每日团费： ($890-$500-$90)/6天=$50\r\n每日出团时间：10小时\r\n每小时团费=($50/10) =$5', '退团费范例:\r\n总团费: $890 \r\n酒店费用: $100/天*5天=$500\r\n巴士费用: $15/天每人*6天*1人 = $90\r\n每日团费： ($890-$500-$90)/6天=$50\r\n每日出团时间：10小时\r\n每小时团费=($50/10) =$5', 1);

-- --------------------------------------------------------

--
-- Table structure for table `mdfy_comments`
--

CREATE TABLE `mdfy_comments` (
  `id` int(15) NOT NULL,
  `cmt_user` varchar(100) DEFAULT NULL,
  `cmt_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `cmt_content` text,
  `qc_num` varchar(20) DEFAULT NULL,
  `case_status` varchar(20) DEFAULT NULL,
  `type` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `mdfy_comments`
--

INSERT INTO `mdfy_comments` (`id`, `cmt_user`, `cmt_date`, `cmt_content`, `qc_num`, `case_status`, `type`) VALUES
(4, 'admin', '2018-02-19 17:04:42', '尊敬的代理,\n非常感谢您将客人的宝贵意见及时地反映给我们！我们会根据这些意见和建议不断地提高我们的服务质量，感谢您一直以来的支持和信任！同时，如果我们的此次服务给您造成任何困扰或不便，我们表示十分抱歉。在收到您的邮件之后，我公司在第一时间询问了相关人员，并根据我们的客户满意保障方案做出了相应的处理意见和处理结果，现告知如下：\n 此单我们愿意退还共计$9的差价。非常抱歉给贵司带来的不便。\n如果您和客人协商后，同意以上赔偿金额，我们有四种方式退款给您：\n1、请您先退款给您的客人，我们会发给您credit memo。\n2、如果客人常居美国，并且有美国的银行账户，我们可以退款到客人的银行账户上，请客人提供以下信息：\n1) 银行名称\n2) 银行账户名字\n3) Account Number\n4) Routing Number\n3、我们可以退款到客人的Chase Quick Pay，请客人提供以下信息：\n1) 账户名称： \n2) 账户邮箱地址或电话号码：\n4、我们可以退款到客人的中国的银行卡上，请客人提供以下信息：\n1) 银行名称\n2) 账户名称\n3) 账户号码\n请将您选择的退款方式告诉我们，一经确认，我们将立即处理退款。\n希望您能对我们的解释表示满意。再次感谢您的支持与理解。如您还有其他意见或建议，欢迎随时与我们联系。', '20180105', 'processing', 'status'),
(5, 'admin', '2018-02-19 17:06:52', '已解决', '20180105', 'solved', 'status'),
(6, 'admin', '2018-02-19 17:07:30', '*必填', '20180105', 'report', 'status'),
(7, 'admin', '2018-02-19 17:36:20', '我是这次的的处理进度', '20180105', NULL, 'processing'),
(8, 'admin', '2018-02-19 17:39:00', '我是这次的处理进度\r\n你好，\r\n我要处理一下进度', '20180105', NULL, 'processing'),
(9, 'admin', '2018-02-22 16:37:05', '1231', '20180105', 'w_email', 'status'),
(10, 'admin', '2018-02-23 14:43:43', '尊敬的代理,\r\n非常感谢您将客人的宝贵意见及时地反映给我们！我们会根据这些意见和建议不断地提高我们的服务质量，感谢您一直以来的支持和信任！同时，如果我们的此次服务给您造成任何困扰或不便，我们表示十分抱歉。在收到您的邮件之后，我公司在第一时间询问了相关人员，并根据我们的客户满意保障方案做出了相应的处理意见和处理结果，现告知如下：\r\n非常抱歉,经核实,是我们这边导游收错，我们愿意退还客人服务费每人差价$3,共$6如造成不便，恳请海涵。请放心，我们会在日后加强管理，避免此类事情发生。\r\n如果您和客人协商后，同意以上赔偿金额，我们有四种方式退款给您：\r\n1、请您先退款给您的客人，我们会发给您credit memo。\r\n2、如果客人常居美国，并且有美国的银行账户，我们可以退款到客人的银行账户上，请客人提供以下信息：\r\n1) 银行名称\r\n2) 银行账户名字\r\n3) Account Number\r\n4) Routing Number\r\n3、我们可以退款到客人的Chase Quick Pay，请客人提供以下信息：\r\n1) 账户名称： \r\n2) 账户邮箱地址或电话号码：\r\n4、我们可以退款到客人的中国的银行卡上，请客人提供以下信息：\r\n1) 银行名称\r\n2) 账户名称\r\n3) 账户号码\r\n请将您选择的退款方式告诉我们，一经确认，我们将立即处理退款。\r\n希望您能对我们的解释表示满意。再次感谢您的支持与理解。如您还有其他意见或建议，欢迎随时与我们联系。', '20180105', NULL, 'processing'),
(11, 'admin', '2018-02-23 14:43:51', '尊敬的客人，\r\n您的手机已于12/29早上寄出。附件是您的包裹的图片。再次感谢您的支持与理解。如您还有其他意见或建议，欢迎随时与我们联系。\r\n\r\n尊敬的客人,\r\n非常感谢您将您的宝贵意见及时地反映给我们！我们会根据这些意见和建议不断地提高我们的服务质量，感谢您一直以来的支持和信任！同时，如果我们的此次服务给您造成任何困扰或不便，我们表示十分抱歉。在收到您的邮件之后，我公司在第一时间询问了相关人员，并根据我们的客户满意保障方案做出了相应的处理意见和处理结果，现告知如下：\r\n经核实，您的手机确实在我们的办公室，我们会替您保留这个手机30天。您可自行来办公室取，如果您需要我们为您邮寄这部手机，烦请提供一个已经付费的shipping label，并且发邮件给我们。关于shipping label,您可自行选择快递公司并且决定是否需要保险因为我们无法保证邮寄的路上物品是否会受损。一旦收到您的shipping label，我们会安排把手机邮寄给您。\r\n再次感谢您的支持与理解。如您还有其他意见或建议，欢迎随时与我们联系。', '20180105', NULL, 'processing'),
(12, 'admin', '2018-02-23 14:44:08', '\r\nDear Customer,\r\nThank you so much for sharing your feedback about our service. We highly value any feedback and suggestion to improve our service quality. Meanwhile, please accept our sincere apology for any inconvenience. On resolving your issue, we are making following explanations and solutions with a thorough investigation. Here is what we have come up with:\r\nRegarding the service of the tour guide, please accept our sincere apology. We are sorry to hear that you feel uncomfortable about our tour guide. For years, we have been focusing on improving customer service. There might be some misunderstandings. Still, we will enhance our regulation on improvement of customer service in future days.\r\nWe are sorry to that our itinerary could not please our customers. It is also our primary goal to arrange each part of itinerary reasonably; moreover, any advice would be possibly taken to increase leisure of tours. In addition, we indeed provide products like charters which are exclusively designated by customers their own. About the itinerary, we will optimize and update it, to make it more well-designed and reasonable. We highly appreciate those suggestions and feedback!\r\nFor this case, there’s no compensation. Thanks again for your support and understanding. We will continuously improve our service quality and customer satisfaction. \r\nIf you still have any other concerns, please feel free to contact us.  Thank you and have a good day!', '20180105', NULL, 'processing'),
(13, 'avawang', '2018-02-23 16:46:15', '气味儿群翁', '122717-1', 'report', 'status'),
(14, 'avawang', '2018-02-23 16:47:21', '尊敬的代理,\r\n非常感谢您将客人的宝贵意见及时地反映给我们！我们会根据这些意见和建议不断地提高我们的服务质量，感谢您一直以来的支持和信任！同时，如果我们的此次服务给您造成任何困扰或不便，我们表示十分抱歉。在收到您的邮件之后，我公司在第一时间询问了相关人员，并根据我们的客户满意保障方案做出了相应的处理意见和处理结果，现告知如下：\r\n 此单我们愿意退还共计$9的差价。非常抱歉给贵司带来的不便。\r\n如果您和客人协商后，同意以上赔偿金额，我们有四种方式退款给您：\r\n1、请您先退款给您的客人，我们会发给您credit memo。\r\n2、如果客人常居美国，并且有美国的银行账户，我们可以退款到客人的银行账户上，请客人提供以下信息：\r\n1) 银行名称\r\n2) 银行账户名字\r\n3) Account Number\r\n4) Routing Number\r\n3、我们可以退款到客人的Chase Quick Pay，请客人提供以下信息：\r\n1) 账户名称： \r\n2) 账户邮箱地址或电话号码：\r\n4、我们可以退款到客人的中国的银行卡上，请客人提供以下信息：\r\n1) 银行名称\r\n2) 账户名称\r\n3) 账户号码\r\n请将您选择的退款方式告诉我们，一经确认，我们将立即处理退款。\r\n希望您能对我们的解释表示满意。再次感谢您的支持与理解。如您还有其他意见或建议，欢迎随时与我们联系。', '122717-1', NULL, 'processing');

-- --------------------------------------------------------

--
-- Table structure for table `order_info`
--

CREATE TABLE `order_info` (
  `id` int(10) NOT NULL,
  `qc_num` varchar(20) DEFAULT NULL,
  `agent` varchar(100) DEFAULT NULL,
  `order_num` varchar(50) DEFAULT NULL,
  `invoice` varchar(30) DEFAULT NULL,
  `departure_date` varchar(20) DEFAULT NULL,
  `room_num` decimal(10,0) NOT NULL DEFAULT '0',
  `tour_guide` varchar(100) DEFAULT NULL,
  `guide_id` varchar(15) DEFAULT NULL,
  `staffs` varchar(500) DEFAULT NULL,
  `staffs_id` varchar(200) DEFAULT NULL,
  `tour_code` varchar(15) DEFAULT NULL,
  `group_code` varchar(15) DEFAULT NULL,
  `pax` int(5) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `order_info`
--

INSERT INTO `order_info` (`id`, `qc_num`, `agent`, `order_num`, `invoice`, `departure_date`, `room_num`, `tour_guide`, `guide_id`, `staffs`, `staffs_id`, `tour_code`, `group_code`, `pax`) VALUES
(1, '20180105', '4', '666555333#', 'EC77777', '2018-01-02', '1', '2', '2', '我是导游;', NULL, 'AP611', 'CC1', 2),
(2, '011818-8', '5', 'DT18-520-0017', 'JE000578', '2018-02-02', '2', '主要导游', '2', '我是导游;', NULL, 'AP9U', 'UR1', 5),
(3, '122717-1', '8', '123066', 'JL003796', '2018-02-15', '11', '主要导游', '2', '我是导游;jing yao;', NULL, 'ap6', '111', 22);

-- --------------------------------------------------------

--
-- Table structure for table `result_info`
--

CREATE TABLE `result_info` (
  `id` int(10) NOT NULL,
  `qc_num` varchar(20) DEFAULT NULL,
  `result` text,
  `payment` varchar(30) DEFAULT NULL,
  `payment_memo` text,
  `compensation_amount` float NOT NULL DEFAULT '0',
  `order_value` float NOT NULL DEFAULT '0',
  `net_income` float NOT NULL DEFAULT '0',
  `resp_party` varchar(100) DEFAULT NULL,
  `satisfaction` varchar(100) DEFAULT NULL,
  `bill` varchar(100) DEFAULT NULL,
  `bill_num` varchar(100) DEFAULT NULL,
  `bill_value` float NOT NULL DEFAULT '0',
  `reference` varchar(100) DEFAULT NULL,
  `analysis` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `result_info`
--

INSERT INTO `result_info` (`id`, `qc_num`, `result`, `payment`, `payment_memo`, `compensation_amount`, `order_value`, `net_income`, `resp_party`, `satisfaction`, `bill`, `bill_num`, `bill_value`, `reference`, `analysis`) VALUES
(6, '20180105', '3123123', 'credit', '1231233', 0, 0, 0, 'agent', 'acceptance', 'hotel', '气温气温翁无群二群翁群', 0, 'compensation', '12312312'),
(7, '122717-1', '31231231', 'cb', '尊敬的代理,\r\n非常感谢您将客人的宝贵意见及时地反映给我们！我们会根据这些意见和建议不断地提高我们的服务质量，感谢您一直以来的支持和信任！同时，如果我们的此次服务给您造成任何困扰或不便，我们表示十分抱歉。在收到您的邮件之后，我公司在第一时间询问了相关人员，并根据我们的客户满意保障方案做出了相应的处理意见和处理结果，现告知如下：\r\n 此单我们愿意退还共计$9的差价。非常抱歉给贵司带来的不便。\r\n如果您和客人协商后，同意以上赔偿金额，我们有四种方式退款给您：\r\n1、请您先退款给您的客人，我们会发给您credit memo。\r\n', 110, 0, 0, 'uv', 'good', 'acc', '123213', 10, 'compensation final', '尊敬的代理,\r\n非常感谢您将客人的宝贵意见及时地反映给我们！我们会根据这些意见和建议不断地提高我们的服务质量，感谢您一直以来的支持和信任！同时，如果我们的此次服务给您造成任何困扰或不便，我们表示十分抱歉。在收到您的邮件之后，我公司在第一时间询问了相关人员，并根据我们的客户满意保障方案做出了相应的处理意见和处理结果，现告知如下：\r\n 此单我们愿意退还共计$9的差价。非常抱歉给贵司带来的不便。\r\n如果您和客人协商后，同意以上赔偿金额，我们有四种方式退款给您：\r\n1、请您先退款给您的客人，我们会发给您credit memo。\r\n2、如果客人常居美国，并且有美国的银行账户，我们可以退款到客人的银行账户上，请客人提供以下信息：\r\n1) 银行名称\r\n2) 银行账户名字\r\n3) Account Number\r\n4) Routing Number\r\n3、我们可以退款到客人的Chase Quick Pay，请客人提供以下信息：\r\n1) 账户名称： \r\n2) 账户邮箱地址或电话号码：\r\n4、我们可以退款到客人的中国的银行卡上，请客人提供以下信息：\r\n1) 银行名称\r\n2) 账户名称\r\n');

-- --------------------------------------------------------

--
-- Table structure for table `user_mgmt`
--

CREATE TABLE `user_mgmt` (
  `id` int(10) NOT NULL,
  `name` varchar(50) DEFAULT NULL,
  `type` varchar(50) DEFAULT NULL,
  `remark` text,
  `is_using` int(1) NOT NULL DEFAULT '1'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Dumping data for table `user_mgmt`
--

INSERT INTO `user_mgmt` (`id`, `name`, `type`, `remark`, `is_using`) VALUES
(1, 'xiaom', 'driver', 'I am the remark', 1),
(2, '我是导游', 'guide', '123', 1),
(3, '你不是导游好好', 'agent', 'driver', 0),
(4, 'agent test', 'agent', 'agent remark', 1),
(5, '代理1', 'agent', 'hhhhhhhhhhhh', 1),
(6, '代理2', 'agent', 'hhhhhhhhhhhh', 1),
(7, '代理3', 'agent', 'hhhhhhhhhhhh', 1),
(8, '代理4', 'agent', 'hhhhhhhhhhhh', 1),
(9, '代理6', 'agent', 'hhhhhhhhhhhh', 1),
(10, '代理7', 'agent', 'hhhhhhhhhhhh', 1),
(11, '代理7', 'agent', 'hhhhhhhhhhhh', 1),
(12, 'jing yao', 'other', 'hhhh', 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `acct_mgmt`
--
ALTER TABLE `acct_mgmt`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `attachment`
--
ALTER TABLE `attachment`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `basic_info`
--
ALTER TABLE `basic_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `label_info`
--
ALTER TABLE `label_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `label_mgmt`
--
ALTER TABLE `label_mgmt`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `mdfy_comments`
--
ALTER TABLE `mdfy_comments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_info`
--
ALTER TABLE `order_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `result_info`
--
ALTER TABLE `result_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `user_mgmt`
--
ALTER TABLE `user_mgmt`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `acct_mgmt`
--
ALTER TABLE `acct_mgmt`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `attachment`
--
ALTER TABLE `attachment`
  MODIFY `id` int(15) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;
--
-- AUTO_INCREMENT for table `basic_info`
--
ALTER TABLE `basic_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
--
-- AUTO_INCREMENT for table `label_info`
--
ALTER TABLE `label_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `label_mgmt`
--
ALTER TABLE `label_mgmt`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
--
-- AUTO_INCREMENT for table `mdfy_comments`
--
ALTER TABLE `mdfy_comments`
  MODIFY `id` int(15) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;
--
-- AUTO_INCREMENT for table `order_info`
--
ALTER TABLE `order_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `result_info`
--
ALTER TABLE `result_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
--
-- AUTO_INCREMENT for table `user_mgmt`
--
ALTER TABLE `user_mgmt`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
