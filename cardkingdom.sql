SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `cardkingdom`
--

-- --------------------------------------------------------

--
-- Table structure for table `cards`
--

CREATE TABLE `cards` (
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `currentName` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `layout` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `manaCost` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `cmc` int(10) NOT NULL,
  `type` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `text` mediumtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `power` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `toughness` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `imageName` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `hiddenId` int(10) DEFAULT NULL,
  `pictureUrl` varchar(160) COLLATE utf8mb4_unicode_ci DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_coloridentity`
--

CREATE TABLE `cards_coloridentity` (
  `identity` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_colors`
--

CREATE TABLE `cards_colors` (
  `color` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_legalities`
--

CREATE TABLE `cards_legalities` (
  `format` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `legality` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_printings`
--

CREATE TABLE `cards_printings` (
  `printing` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_rulings`
--

CREATE TABLE `cards_rulings` (
  `ruling` int(10) NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date` date NOT NULL,
  `text` text COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_subtypes`
--

CREATE TABLE `cards_subtypes` (
  `subtype` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(160) COLLATE utf8mb4_unicode_ci NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cards_types`
--

CREATE TABLE `cards_types` (
  `type` varchar(160) CHARACTER SET latin1 NOT NULL,
  `name` varchar(160) CHARACTER SET latin1 NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `cards`
--
ALTER TABLE `cards`
  ADD PRIMARY KEY (`name`(142));

--
-- Indexes for table `cards_coloridentity`
--
ALTER TABLE `cards_coloridentity`
  ADD PRIMARY KEY (`identity`,`name`);

--
-- Indexes for table `cards_colors`
--
ALTER TABLE `cards_colors`
  ADD PRIMARY KEY (`color`,`name`);

--
-- Indexes for table `cards_legalities`
--
ALTER TABLE `cards_legalities`
  ADD PRIMARY KEY (`format`,`name`);

--
-- Indexes for table `cards_printings`
--
ALTER TABLE `cards_printings`
  ADD PRIMARY KEY (`printing`,`name`);

--
-- Indexes for table `cards_rulings`
--
ALTER TABLE `cards_rulings`
  ADD PRIMARY KEY (`ruling`,`name`);

--
-- Indexes for table `cards_subtypes`
--
ALTER TABLE `cards_subtypes`
  ADD PRIMARY KEY (`subtype`,`name`);

--
-- Indexes for table `cards_types`
--
ALTER TABLE `cards_types`
  ADD PRIMARY KEY (`type`,`name`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;