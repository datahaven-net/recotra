# RECOTRA

RECOTRA	= REgulatory COmpliant TRAder
This software facilitates in person Bitcoin trading with paper contracts with QR codes.
It also helps with Regulatory Compliance requirements for KYC and AML.
One person with a computer, printer, scanner, webcam can trade Bitcoin with in person customers.
You can provide the same service as a "Bitcoin ATM" with far lower capital costs.
It is also much easier to keep in operation than an ATM.

Link to Video showing use of this software coming here soon:   

Regulators classify this under VASP - Virtual Asset Service Provider


A tool for accounting BTC exchange contracts

Uses Kivy framework to render user interface

At first clone the files locally and change to the repository folder:

		git clone https://github.com/datahaven-net/btc-simple-contracts.git
		cd btc-simple-contracts


To be able to run the application from command line you must first install Kivy dependencies (tested on Linux Debian) and create Python virtual environment:

		make clean install


Also to make sure you are running the most recent version you can run following command that will use Git to fetch latest commits from GitHub:

		make update


Then you should be able to start the application inside development environment:

		make run
