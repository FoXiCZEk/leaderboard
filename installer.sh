#!/bin/bash

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

SQL_CREATE_DB="CREATE DATABASE dayz_leaderboard;"
SQL_CREATE_TABLE1='CREATE TABLE `dayz_players` (`id` int(11) NOT NULL AUTO_INCREMENT,`steamId` varchar(18) DEFAULT NULL,`deaths` int(11) DEFAULT NULL,`kills` int(11) DEFAULT NULL,`animalsKilled` int(11) DEFAULT NULL,`name` varchar(100) DEFAULT NULL,`lastTimeSeen` timestamp NULL DEFAULT NULL,`deathsToZCount` int(11) DEFAULT NULL,`deathsToNaturalCauseCount` int(11) DEFAULT NULL,`deathsToPlayerCount` int(11) DEFAULT NULL,`deathsToAnimalCount` int(11) DEFAULT NULL,`suicideCount` int(11) DEFAULT NULL,`longestShot` int(11) DEFAULT NULL,`zKilled` int(11) DEFAULT NULL,`timeSurvived` int(11) DEFAULT NULL,`distTrav` int(11) DEFAULT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=82 DEFAULT CHARSET=latin1'
SQL_CREATE_TABLE2='CREATE TABLE `dayz_death` (`id` int(11) NOT NULL AUTO_INCREMENT,`steamId` varchar(18) DEFAULT NULL,`animalsKilled` int(11) DEFAULT NULL,`kills` int(11) DEFAULT NULL,`longestShot` int(11) DEFAULT NULL,`timeSurvived` int(11) DEFAULT NULL,`zKillCount` int(11) DEFAULT NULL,`distTrav` int(11) DEFAULT NULL,`timeStamp` timestamp NULL DEFAULT NULL,`posDeath` varchar(150) DEFAULT NULL,`killer` varchar(100) DEFAULT NULL,`weapon` varchar(100) DEFAULT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=106 DEFAULT CHARSET=latin1'
SQL_CREATE_TABLE3='CREATE ALGORITHM=UNDEFINED DEFINER=`dayz_leaderboard`@`%` SQL SECURITY DEFINER VIEW `dayz_death_player` AS select `dayz_death`.`id` AS `id`,`dayz_players`.`name` AS `name`,`dayz_death`.`animalsKilled` AS `animalsKilled`,`dayz_death`.`kills` AS `kills`,`dayz_death`.`longestShot` AS `longestShot`,sec_to_time(`dayz_death`.`timeSurvived`) AS `timeSurvived`,`dayz_death`.`zKillCount` AS `zKillCount`,`dayz_death`.`distTrav` AS `distTrav`,`dayz_death`.`killer` AS `killer`,`dayz_death`.`weapon` AS `weapon` from (`dayz_death` join `dayz_players` on(`dayz_death`.`steamId` = `dayz_players`.`steamId`))'

PIP_REQUIREMENTS="virtualenv"
PIP_REQUIREMENTS_DJANGO="django django-tables2 requests mysql-connector mysqlclient mysql mysqlx"

OS_APACHE2="apache2 apache2-utils ssl-cert libapache2-mod-wsgi-py3 libmariadb-dev python3-pip"

logger(){
	if [ $1 == "ERROR" ];then
		echo -e "[${RED}$1${ENDCOLOR}] $2"
    exit 1
	else
		echo -e "[${GREEN}$1${ENDCOLOR}] $2"	
	fi
}

if [ `whoami` != "root" ];then
    logger ERROR "please run installer with root privileges"
fi

echo -ne 'mysql username : '
read mysql_user
echo -ne 'mysql password : '
read -s mysql_pass
echo -e "\n"
logger INFO "#### MySQL CONFIGURATION ####"
mysql -u ${mysql_user} -p${mysql_pass} -e "show databases;" || logger ERROR "MysqlError ocured"
logger INFO "SQL Account looks OK."
logger INFO "Creating database dayz_leaderboard"
mysql -u ${mysql_user} -p${mysql_pass} -e "${SQL_CREATE_DB}" || logger ERROR "MySQL unable to create database"
logger INFO "Creating table dayz_players"
mysql -u ${mysql_user} -p${mysql_pass} -e "${SQL_CREATE_TABLE1}" dayz_leaderboard || logger ERROR "MySQL unable to create table dayz_players"
logger INFO "Creating table dayz_death"
mysql -u ${mysql_user} -p${mysql_pass} -e "${SQL_CREATE_TABLE2}" dayz_leaderboard || logger ERROR "MySQL unable to create table dayz_death"
logger INFO "Creating table dayz_death_player"
mysql -u ${mysql_user} -p${mysql_pass} -e "${SQL_CREATE_TABLE3}" dayz_leaderboard || logger ERROR "MySQL unable to create table dayz_death_player"
logger INFO "Granting MySQL privileges"
mysql -u ${mysql_user} -p${mysql_pass} -e "GRANT ALL ON dayz_leaderboard.* TO dayz_leaderboard@'%' IDENTIFIED BY 'Ostrava123';" dayz_leaderboard || logger ERROR "MySQL unable to grant privileges" 
logger INFO "MySQL preparation complete"

logger INFO "#### PYTHON3 CONFIGURATION ####"
apt install -y ${OS_APACHE2} || logger ERROR "Problem with installing OS packages"
pip3 install ${PIP_REQUIREMENTS} || logger ERROR "unable to install pip3 requirements"

logger INFO "#### WEB DEPLOYMENT ####"
pip3 install ${PIP_REQUIREMENTS_DJANGO} || logger ERROR "unable to install python3 django modules"
cd /var/www
git clone https://github.com/FoXiCZEk/leaderboard.git || logger ERROR "unable to clone from github"
cd /var/www/leaderboard
virtualenv venv || logger ERROR "unable co create virtual environment"
cd /var/www/leaderboard/venv/bin
. ./activate
pip3 install ${PIP_REQUIREMENTS_DJANGO} || logger ERROR "unable to install python3 django modules"

logger INFO "#### APACHE2 CONFIGURATION ####"

if [ -f /etc/apache2/conf-available/002_leaderboard.conf ];then
    logger INFO "found apache2 configuration file"
else
    logger INFO "creating apache2 configuration file"
    mv /var/www/leaderboard/002_leaderboard.conf /etc/apache2/conf-available/002_leaderboard.conf || logger ERROR "unable to create apache2 configuration file"
fi
logger INFO "enabling apache2 configuration"
a2enconf 002_leaderboard.conf || logger ERROR "unable to enable apache2 configuration"
