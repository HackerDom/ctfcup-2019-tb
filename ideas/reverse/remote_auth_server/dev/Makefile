all:
	g++ sha256.cpp source.cpp -o ras -static
	strip ras
	upx -9 ras
	python upx_eraser.py ras