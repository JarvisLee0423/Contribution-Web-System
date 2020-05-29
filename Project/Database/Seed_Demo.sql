-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2020-05-19 13:08:59
-- 服务器版本： 10.1.38-MariaDB
-- PHP 版本： 7.3.3

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `seed`
--

-- --------------------------------------------------------

--
-- 表的结构 `belongto`
--

CREATE TABLE `belongto` (
  `userID` varchar(255) NOT NULL,
  `submissionID` int(11) NOT NULL,
  `contribution` float NOT NULL DEFAULT '-1'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `belongto`
--

INSERT INTO `belongto` (`userID`, `submissionID`, `contribution`) VALUES
('m370026007', 3, 1),
('m370026007', 4, 1),
('m370026025', 3, 0.33),
('m370026025', 4, 0),
('m370026041', 3, 0),
('m370026041', 4, 1),
('m370026042', 3, 1),
('m370026042', 4, 1),
('m370026043', 3, 0.67),
('m370026043', 4, 0.67),
('m370026044', 3, 1),
('m370026044', 4, 1),
('m370026045', 3, 0.67),
('m370026045', 4, 0.67),
('m370026046', 3, 0),
('m370026046', 4, 1),
('m370026047', 3, 1),
('m370026047', 4, 1),
('m370026048', 3, 0.67),
('m370026048', 4, 0.33),
('m370026066', 3, 1),
('m370026066', 4, 1),
('m370026071', 3, 0.67),
('m370026071', 4, 0.33),
('m370026098', 3, 1),
('m370026098', 4, 1),
('m370026123', 3, 0.67),
('m370026123', 4, 0.67),
('m370026155', 3, 1),
('m370026155', 4, 1),
('m370026157', 3, 0.67),
('m370026157', 4, 0.67);

-- --------------------------------------------------------

--
-- 表的结构 `course`
--

CREATE TABLE `course` (
  `courseID` varchar(255) NOT NULL,
  `courseName` varchar(255) NOT NULL,
  `numOfStudent` int(11) NOT NULL DEFAULT '0',
  `formTeamMethod` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `course`
--

INSERT INTO `course` (`courseID`, `courseName`, `numOfStudent`, `formTeamMethod`) VALUES
('DB1001', 'Database Instructions', 16, NULL),
('DL1001', 'Deep Learning', 0, NULL),
('ENGLISH1001', 'Applied English', 0, NULL),
('ML1001', 'Machine Learning in AI', 16, '[\'B\', -1, 4]'),
('PYTHON1001', 'Python Programming', 16, NULL),
('SDW1001', 'Software Development Workshop', 16, '[\'E\', 2, 4]'),
('SDW1002', 'Software Development Workshop', 17, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `has`
--

CREATE TABLE `has` (
  `courseID` varchar(255) NOT NULL,
  `teamID` int(11) NOT NULL,
  `numOfStudent` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `has`
--

INSERT INTO `has` (`courseID`, `teamID`, `numOfStudent`) VALUES
('ML1001', 14, 4),
('ML1001', 15, 4),
('ML1001', 16, 4),
('ML1001', 17, 4),
('SDW1001', 10, 4),
('SDW1001', 11, 4),
('SDW1001', 12, 4),
('SDW1001', 13, 4);

-- --------------------------------------------------------

--
-- 表的结构 `leader`
--

CREATE TABLE `leader` (
  `userID` varchar(255) NOT NULL,
  `teamID` int(11) NOT NULL,
  `bonus` float DEFAULT '0',
  `tempBonus` varchar(255) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `leader`
--

INSERT INTO `leader` (`userID`, `teamID`, `bonus`, `tempBonus`) VALUES
('m370026042', 12, 0, '0'),
('m370026045', 11, 0, '0'),
('m370026047', 10, 0, '0'),
('m370026098', 13, 0, '0');

-- --------------------------------------------------------

--
-- 表的结构 `member`
--

CREATE TABLE `member` (
  `userID` varchar(255) NOT NULL,
  `teamID` int(11) NOT NULL,
  `courseID` varchar(255) NOT NULL,
  `contribution` float DEFAULT '0',
  `state` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `member`
--

INSERT INTO `member` (`userID`, `teamID`, `courseID`, `contribution`, `state`) VALUES
('m370026007', 10, 'SDW1001', 1, 1),
('m370026007', 17, 'ML1001', 1, 0),
('m370026025', 10, 'SDW1001', 0.17, 1),
('m370026025', 14, 'ML1001', 1, 0),
('m370026041', 13, 'SDW1001', 0.5, 1),
('m370026041', 15, 'ML1001', 1, 0),
('m370026042', 12, 'SDW1001', 1, 1),
('m370026042', 16, 'ML1001', 1, 0),
('m370026043', 10, 'SDW1001', 0.67, 1),
('m370026043', 17, 'ML1001', 1, 0),
('m370026044', 11, 'SDW1001', 1, 1),
('m370026044', 14, 'ML1001', 1, 0),
('m370026045', 11, 'SDW1001', 0.67, 1),
('m370026045', 15, 'ML1001', 1, 0),
('m370026046', 11, 'SDW1001', 0.5, 1),
('m370026046', 16, 'ML1001', 1, 0),
('m370026047', 10, 'SDW1001', 1, 1),
('m370026047', 15, 'ML1001', 1, 0),
('m370026048', 13, 'SDW1001', 0.5, 1),
('m370026048', 16, 'ML1001', 1, 0),
('m370026066', 11, 'SDW1001', 1, 1),
('m370026066', 14, 'ML1001', 1, 0),
('m370026071', 12, 'SDW1001', 0.5, 1),
('m370026071', 16, 'ML1001', 1, 0),
('m370026098', 13, 'SDW1001', 1, 1),
('m370026098', 15, 'ML1001', 1, 0),
('m370026123', 13, 'SDW1001', 0.67, 1),
('m370026123', 17, 'ML1001', 1, 0),
('m370026155', 12, 'SDW1001', 1, 1),
('m370026155', 14, 'ML1001', 1, 0),
('m370026157', 12, 'SDW1001', 0.67, 1),
('m370026157', 17, 'ML1001', 1, 0);

-- --------------------------------------------------------

--
-- 表的结构 `ownedby`
--

CREATE TABLE `ownedby` (
  `courseID` varchar(255) NOT NULL,
  `submissionID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `ownedby`
--

INSERT INTO `ownedby` (`courseID`, `submissionID`) VALUES
('ML1001', 1),
('ML1001', 2),
('SDW1001', 3),
('SDW1001', 4);

-- --------------------------------------------------------

--
-- 表的结构 `pairs`
--

CREATE TABLE `pairs` (
  `pairsID` int(11) NOT NULL,
  `inviterID` varchar(255) NOT NULL,
  `inviteeID` varchar(255) NOT NULL,
  `courseID` varchar(255) NOT NULL,
  `avgGPA` float DEFAULT '0',
  `state` int(11) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `student`
--

CREATE TABLE `student` (
  `userID` varchar(255) NOT NULL,
  `userName` varchar(8) DEFAULT NULL,
  `password` varchar(16) NOT NULL DEFAULT '11111111',
  `programme` varchar(255) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phoneNumber` varchar(11) DEFAULT NULL,
  `GPA` float NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `student`
--

INSERT INTO `student` (`userID`, `userName`, `password`, `programme`, `name`, `email`, `phoneNumber`, `GPA`) VALUES
('m370026007', 'Franky', '11111111', '', 'Franky', 'm730026007@mail.uic.edu.hk', '', 2.67),
('m370026025', 'Dan', '11111111', '', 'Dan', 'm730026025@mail.uic.edu.hk', '', 3.3),
('m370026041', 'Alex', '11111111', '', 'Alex', 'm730026041@mail.uic.edu.hk', '', 3.17),
('m370026042', 'Jarvis', '11111111', '', 'Jarvis', 'm730026042@mail.uic.edu.hk', '', 3.3),
('m370026043', 'Blank', '11111111', '', 'Blank', 'm730026043@mail.uic.edu.hk', '', 2.33),
('m370026044', 'Jay', '11111111', '', 'Jay', 'm730026044@mail.uic.edu.hk', '', 3.82),
('m370026045', 'Jerry', '11111111', '', 'Jerry', 'm730026045@mail.uic.edu.hk', '', 3.77),
('m370026046', 'Marry', '11111111', '', 'Marry', 'm730026046@mail.uic.edu.hk', '', 2.46),
('m370026047', 'Judy', '11111111', '', 'Judy', 'm730026047@mail.uic.edu.hk', '', 3.9),
('m370026048', 'Sandy', '11111111', '', 'Sandy', 'm730026048@mail.uic.edu.hk', '', 2.79),
('m370026066', 'Bob', '11111111', '', 'Bob', 'm730026066@mail.uic.edu.hk', '', 2.87),
('m370026071', 'Andy', '11111111', '', 'Andy', 'm730026071@mail.uic.edu.hk', '', 3.23),
('m370026098', 'Hillary', '11111111', '', 'Hillary', 'm730026098@mail.uic.edu.hk', '', 3.97),
('m370026123', 'Banana', '11111111', '', 'Banana', 'm730026123@mail.uic.edu.hk', '', 3),
('m370026155', 'Virgil', '11111111', '', 'Virgil', 'm730026155@mail.uic.edu.hk', '', 3.3),
('m370026157', 'Bill', '11111111', '', 'Bill', 'm730026157@mail.uic.edu.hk', '', 3.3),
('m730026233', 'Branda', '11111111', '', 'Branda', 'm730026233@mail.uic.edu.hk', '', 2.42);

-- --------------------------------------------------------

--
-- 表的结构 `submission`
--

CREATE TABLE `submission` (
  `submissionID` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `percentage` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `submission`
--

INSERT INTO `submission` (`submissionID`, `title`, `percentage`) VALUES
(1, 'Doucumentation', 0.5),
(2, 'Project', 0.5),
(3, 'Project', 0.5),
(4, 'Coding', 0.5);

-- --------------------------------------------------------

--
-- 表的结构 `takenby`
--

CREATE TABLE `takenby` (
  `courseID` varchar(255) NOT NULL,
  `userID` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `takenby`
--

INSERT INTO `takenby` (`courseID`, `userID`) VALUES
('DB1001', 'm370026007'),
('DB1001', 'm370026025'),
('DB1001', 'm370026041'),
('DB1001', 'm370026042'),
('DB1001', 'm370026043'),
('DB1001', 'm370026044'),
('DB1001', 'm370026045'),
('DB1001', 'm370026046'),
('DB1001', 'm370026047'),
('DB1001', 'm370026048'),
('DB1001', 'm370026066'),
('DB1001', 'm370026071'),
('DB1001', 'm370026098'),
('DB1001', 'm370026123'),
('DB1001', 'm370026155'),
('DB1001', 'm370026157'),
('ML1001', 'm370026007'),
('ML1001', 'm370026025'),
('ML1001', 'm370026041'),
('ML1001', 'm370026042'),
('ML1001', 'm370026043'),
('ML1001', 'm370026044'),
('ML1001', 'm370026045'),
('ML1001', 'm370026046'),
('ML1001', 'm370026047'),
('ML1001', 'm370026048'),
('ML1001', 'm370026066'),
('ML1001', 'm370026071'),
('ML1001', 'm370026098'),
('ML1001', 'm370026123'),
('ML1001', 'm370026155'),
('ML1001', 'm370026157'),
('PYTHON1001', 'm370026007'),
('PYTHON1001', 'm370026025'),
('PYTHON1001', 'm370026041'),
('PYTHON1001', 'm370026042'),
('PYTHON1001', 'm370026043'),
('PYTHON1001', 'm370026044'),
('PYTHON1001', 'm370026045'),
('PYTHON1001', 'm370026046'),
('PYTHON1001', 'm370026047'),
('PYTHON1001', 'm370026048'),
('PYTHON1001', 'm370026066'),
('PYTHON1001', 'm370026071'),
('PYTHON1001', 'm370026098'),
('PYTHON1001', 'm370026123'),
('PYTHON1001', 'm370026155'),
('PYTHON1001', 'm370026157'),
('SDW1001', 'm370026007'),
('SDW1001', 'm370026025'),
('SDW1001', 'm370026041'),
('SDW1001', 'm370026042'),
('SDW1001', 'm370026043'),
('SDW1001', 'm370026044'),
('SDW1001', 'm370026045'),
('SDW1001', 'm370026046'),
('SDW1001', 'm370026047'),
('SDW1001', 'm370026048'),
('SDW1001', 'm370026066'),
('SDW1001', 'm370026071'),
('SDW1001', 'm370026098'),
('SDW1001', 'm370026123'),
('SDW1001', 'm370026155'),
('SDW1001', 'm370026157');

-- --------------------------------------------------------

--
-- 表的结构 `taught`
--

CREATE TABLE `taught` (
  `courseID` varchar(255) NOT NULL,
  `userID` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `taught`
--

INSERT INTO `taught` (`courseID`, `userID`) VALUES
('DB1001', 'Nina'),
('DL1001', 'Nina'),
('ENGLISH1001', 'Adam'),
('ML1001', 'Nina'),
('PYTHON1001', 'Nina'),
('SDW1001', 'Nina'),
('SDW1002', 'Jim');

-- --------------------------------------------------------

--
-- 表的结构 `teacher`
--

CREATE TABLE `teacher` (
  `userID` varchar(255) NOT NULL,
  `userName` varchar(8) DEFAULT NULL,
  `password` varchar(16) NOT NULL,
  `programme` varchar(255) DEFAULT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `phoneNumber` varchar(11) DEFAULT NULL,
  `officeNumber` varchar(255) DEFAULT NULL,
  `officePhoneNumber` varchar(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `teacher`
--

INSERT INTO `teacher` (`userID`, `userName`, `password`, `programme`, `name`, `email`, `phoneNumber`, `officeNumber`, `officePhoneNumber`) VALUES
('Adam', 'Adam', 'Adam1001', 'ELLS', 'Adam', 'adam@uic.edu.hk', NULL, NULL, NULL),
('Jim', 'Jim', 'Jim1002', 'CST', 'Jim', 'jim@uic.edu.hk', NULL, NULL, NULL),
('Nina', 'Nina', 'Nina1001', 'CST', 'Nina', 'nina@uic.edu.hk', NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `team`
--

CREATE TABLE `team` (
  `teamID` int(11) NOT NULL,
  `teamNumber` int(11) NOT NULL,
  `teamName` varchar(255) DEFAULT NULL,
  `numOfMember` int(11) NOT NULL,
  `leaderState` varchar(255) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- 转存表中的数据 `team`
--

INSERT INTO `team` (`teamID`, `teamNumber`, `teamName`, `numOfMember`, `leaderState`) VALUES
(10, 1, NULL, 4, '1'),
(11, 2, NULL, 4, '1'),
(12, 3, NULL, 4, '1'),
(13, 4, NULL, 4, '1'),
(14, 1, NULL, 4, '0'),
(15, 2, NULL, 4, '0'),
(16, 3, NULL, 4, '0'),
(17, 4, NULL, 4, '0');

--
-- 转储表的索引
--

--
-- 表的索引 `belongto`
--
ALTER TABLE `belongto`
  ADD PRIMARY KEY (`userID`,`submissionID`),
  ADD KEY `submissionID` (`submissionID`);

--
-- 表的索引 `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`courseID`);

--
-- 表的索引 `has`
--
ALTER TABLE `has`
  ADD PRIMARY KEY (`courseID`,`teamID`),
  ADD KEY `teamID` (`teamID`);

--
-- 表的索引 `leader`
--
ALTER TABLE `leader`
  ADD PRIMARY KEY (`userID`,`teamID`),
  ADD KEY `teamID` (`teamID`);

--
-- 表的索引 `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`userID`,`teamID`),
  ADD KEY `teamID` (`teamID`),
  ADD KEY `courseID` (`courseID`);

--
-- 表的索引 `ownedby`
--
ALTER TABLE `ownedby`
  ADD PRIMARY KEY (`courseID`,`submissionID`),
  ADD KEY `submissionID` (`submissionID`);

--
-- 表的索引 `pairs`
--
ALTER TABLE `pairs`
  ADD PRIMARY KEY (`pairsID`);

--
-- 表的索引 `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`userID`,`email`);

--
-- 表的索引 `submission`
--
ALTER TABLE `submission`
  ADD PRIMARY KEY (`submissionID`);

--
-- 表的索引 `takenby`
--
ALTER TABLE `takenby`
  ADD PRIMARY KEY (`courseID`,`userID`),
  ADD KEY `userID` (`userID`);

--
-- 表的索引 `taught`
--
ALTER TABLE `taught`
  ADD PRIMARY KEY (`courseID`,`userID`),
  ADD KEY `userID` (`userID`);

--
-- 表的索引 `teacher`
--
ALTER TABLE `teacher`
  ADD PRIMARY KEY (`userID`);

--
-- 表的索引 `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`teamID`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `pairs`
--
ALTER TABLE `pairs`
  MODIFY `pairsID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `submission`
--
ALTER TABLE `submission`
  MODIFY `submissionID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用表AUTO_INCREMENT `team`
--
ALTER TABLE `team`
  MODIFY `teamID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- 限制导出的表
--

--
-- 限制表 `belongto`
--
ALTER TABLE `belongto`
  ADD CONSTRAINT `belongto_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `member` (`userID`),
  ADD CONSTRAINT `belongto_ibfk_2` FOREIGN KEY (`submissionID`) REFERENCES `submission` (`submissionID`);

--
-- 限制表 `has`
--
ALTER TABLE `has`
  ADD CONSTRAINT `has_ibfk_1` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`),
  ADD CONSTRAINT `has_ibfk_2` FOREIGN KEY (`teamID`) REFERENCES `team` (`teamID`);

--
-- 限制表 `leader`
--
ALTER TABLE `leader`
  ADD CONSTRAINT `leader_ibfk_1` FOREIGN KEY (`teamID`) REFERENCES `team` (`teamID`),
  ADD CONSTRAINT `leader_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `student` (`userID`);

--
-- 限制表 `member`
--
ALTER TABLE `member`
  ADD CONSTRAINT `member_ibfk_1` FOREIGN KEY (`teamID`) REFERENCES `team` (`teamID`),
  ADD CONSTRAINT `member_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `student` (`userID`),
  ADD CONSTRAINT `member_ibfk_3` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`);

--
-- 限制表 `ownedby`
--
ALTER TABLE `ownedby`
  ADD CONSTRAINT `ownedby_ibfk_1` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`),
  ADD CONSTRAINT `ownedby_ibfk_2` FOREIGN KEY (`submissionID`) REFERENCES `submission` (`submissionID`);

--
-- 限制表 `takenby`
--
ALTER TABLE `takenby`
  ADD CONSTRAINT `takenby_ibfk_1` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`),
  ADD CONSTRAINT `takenby_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `student` (`userID`);

--
-- 限制表 `taught`
--
ALTER TABLE `taught`
  ADD CONSTRAINT `taught_ibfk_1` FOREIGN KEY (`courseID`) REFERENCES `course` (`courseID`),
  ADD CONSTRAINT `taught_ibfk_2` FOREIGN KEY (`userID`) REFERENCES `teacher` (`userID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
