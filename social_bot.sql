-- phpMyAdmin SQL Dump
-- version 2.11.6
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Mar 14, 2022 at 05:06 AM
-- Server version: 5.0.51
-- PHP Version: 5.2.6

SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Database: `social_bot`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `username` varchar(20) NOT NULL,
  `password` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`username`, `password`) VALUES
('admin', 'admin');

-- --------------------------------------------------------

--
-- Table structure for table `register`
--

CREATE TABLE `register` (
  `id` int(11) NOT NULL,
  `name` varchar(20) NOT NULL,
  `gender` varchar(10) NOT NULL,
  `dob` varchar(20) NOT NULL,
  `mobile` bigint(20) NOT NULL,
  `email` varchar(40) NOT NULL,
  `location` varchar(30) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `pass` varchar(20) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `profession` varchar(30) NOT NULL,
  `aadhar` varchar(20) NOT NULL,
  `photo` int(11) NOT NULL,
  `status` int(11) NOT NULL,
  `dstatus` int(11) NOT NULL,
  PRIMARY KEY  (`uname`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `register`
--

INSERT INTO `register` (`id`, `name`, `gender`, `dob`, `mobile`, `email`, `location`, `uname`, `pass`, `rdate`, `profession`, `aadhar`, `photo`, `status`, `dstatus`) VALUES
(3, 'Priya', 'Female', '1995-07-03', 7834520187, 'priya@gmail.com', 'Madurai', 'priya', '1234', '14-03-2022', 'Model', '456810983482', 1, 0, 1),
(1, 'Ram', 'Male', '1993-04-12', 9088076557, 'ram@gmail.com', 'Chennai', 'ram', '1234', '13-03-2022', 'Software', '567843215678', 1, 1, 0),
(2, 'Surya', 'Male', '1999-06-04', 8867844201, 'surya@gmail.com', 'Bangalore', 'surya', '1234', '14-03-2022', 'Music', '678853767192', 1, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `user_post`
--

CREATE TABLE `user_post` (
  `id` int(11) NOT NULL,
  `uname` varchar(20) NOT NULL,
  `text_post` varchar(200) NOT NULL,
  `photo` varchar(50) NOT NULL,
  `rdate` varchar(15) NOT NULL,
  `status` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `user_post`
--

INSERT INTO `user_post` (`id`, `uname`, `text_post`, `photo`, `rdate`, `status`) VALUES
(1, 'ram', 'hi, welcome', '', '14-03-2022', 0),
(2, 'priya', 'I am just me being ME!!', '', '14-03-2022', 1),
(3, 'priya', 'I am interested in science, music, art, and i am slightly insane', '', '14-03-2022', 1),
(4, 'priya', 'Very Asian xD', '', '14-03-2022', 1),
(5, 'priya', 'Canal de noticias 24 horas de', '', '14-03-2022', 1),
(6, 'priya', 'Less than somebody, more than nobody.', '', '14-03-2022', 1),
(7, 'surya', 'new technology', 'P7satc4.jpeg', '14-03-2022', 0),
(8, 'priya', 'I tweet historical newspapers', '', '14-03-2022', 1);
