-- phpMyAdmin SQL Dump
-- version 4.8.5
-- https://www.phpmyadmin.net/
--
-- 主机： 127.0.0.1
-- 生成日期： 2020-05-16 14:39:53
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
('DB1001', 'Database Instructions', 0, NULL),
('DL1001', 'Deep Learning', 0, NULL),
('ENGLISH1001', 'Applied English', 0, NULL),
('ML1001', 'Machine Learning', 0, NULL),
('PYTHON1001', 'Python Programming', 4, NULL),
('SDW1001', 'Software Development Workshop', 0, NULL),
('SDW1002', 'Software Development Workshop', 5, NULL);

-- --------------------------------------------------------

--
-- 表的结构 `has`
--

CREATE TABLE `has` (
  `courseID` varchar(255) NOT NULL,
  `teamID` int(11) NOT NULL,
  `numOfStudent` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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

-- --------------------------------------------------------

--
-- 表的结构 `ownedby`
--

CREATE TABLE `ownedby` (
  `courseID` varchar(255) NOT NULL,
  `submissionID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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

-- --------------------------------------------------------

--
-- 表的结构 `submission`
--

CREATE TABLE `submission` (
  `submissionID` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `percentage` float NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- 表的结构 `takenby`
--

CREATE TABLE `takenby` (
  `courseID` varchar(255) NOT NULL,
  `userID` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

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
('DB1001', 'Jim'),
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
  MODIFY `submissionID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `team`
--
ALTER TABLE `team`
  MODIFY `teamID` int(11) NOT NULL AUTO_INCREMENT;

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
