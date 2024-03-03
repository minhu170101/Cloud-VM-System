-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 05, 2023 at 05:16 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `openstack`
--

-- --------------------------------------------------------

--
-- Table structure for table `mayvatly`
--

CREATE TABLE `mayvatly` (
  `id` int(11) NOT NULL,
  `name` text NOT NULL,
  `MAC_addr` text NOT NULL,
  `ngay_tao` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `mayvatly`
--

INSERT INTO `mayvatly` (`id`, `name`, `MAC_addr`, `ngay_tao`) VALUES
(1, 'Máy 01', '0255ff5de9028ae4c96a', '2023-11-04 10:18:52'),
(2, 'Máy 02', 'b0015f2eaa3e6d47fb03', '2023-11-04 10:18:57'),
(3, 'Máy 03', '190d185b7880d5c90276', '2023-11-04 10:19:06'),
(4, 'Máy 04', 'b8ba77acdfb6fbe52780', '2023-11-04 10:19:11'),
(6, 'MinhPC', '11c006f37a665816763d', '2023-11-05 09:43:01');

-- --------------------------------------------------------

--
-- Table structure for table `quyentruycap`
--

CREATE TABLE `quyentruycap` (
  `id` int(11) NOT NULL,
  `VM_id` text NOT NULL,
  `VM_name` text NOT NULL,
  `PM_name` text NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL,
  `ip_addr` text NOT NULL,
  `mac_addr` text NOT NULL,
  `time_log` timestamp NULL DEFAULT NULL,
  `ngay_cap` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `quyentruycap`
--

INSERT INTO `quyentruycap` (`id`, `VM_id`, `VM_name`, `PM_name`, `username`, `password`, `ip_addr`, `mac_addr`, `time_log`, `ngay_cap`) VALUES
(3, '77997092-df12-44cf-9c0b-8b2035cc57c2', 'PC02', 'Máy 03', 'FIT2', 'FIT2', '172.24.4.64', '190d185b7880d5c90276', NULL, '2023-11-05 09:27:14'),
(4, '364fce21-5d76-46b0-b53f-080fa6ea6082', 'PC03', 'Máy 04', 'FIT2', 'FIT2', '172.24.4.181', 'b8ba77acdfb6fbe52780', NULL, '2023-11-05 09:27:19'),
(5, '10bc6a2d-69c9-44a5-bd96-b04a0a8dfb47', 'PC01', 'Máy 01', 'FIT2', 'FIT2', '172.24.4.195', '0255ff5de9028ae4c96a', NULL, '2023-11-05 09:30:54'),
(8, '10bc6a2d-69c9-44a5-bd96-b04a0a8dfb47', 'PC01', 'MinhPC', 'FIT', 'FIT', '172.24.4.195', '11c006f37a665816763d', NULL, '2023-11-05 09:44:43');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `username` text NOT NULL,
  `password` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `username`, `password`) VALUES
(1, 'minh', 'minh');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `mayvatly`
--
ALTER TABLE `mayvatly`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `quyentruycap`
--
ALTER TABLE `quyentruycap`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `mayvatly`
--
ALTER TABLE `mayvatly`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `quyentruycap`
--
ALTER TABLE `quyentruycap`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
