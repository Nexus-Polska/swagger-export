# swagger-export


Swagger-export is a simple application that allows you to generate pdf or html files from the swagger.json definition file. It requires docker with linux containers.

## Build

```
make
```

On Windows, you can install `make` with the [Chocolatey](https://chocolatey.org/install):
```
choco install make
```

## Usage

### Pdf generation from file

Place your swagger definition file in the `work` directory.

```
./swagger-export.sh pdf --file swagger.json
```

### Pdf generation from url
```
./swagger-export.sh pdf --url http://example.com/api/swagger.json
```

### Html generation from file

```
./swagger-export.sh html --file swagger.json
```

### Html generation from url
```
./swagger-export.sh html --url http://example.com/api/swagger.json
```
