IMG:=nxpl/swaggerexport

build:
	docker build -t $(IMG) .

clean:
	docker rmi $(IMG)
