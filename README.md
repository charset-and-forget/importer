# Objective

This repositiry created specifically for RebelMouse clients who is willing to perform content import from their current platform to RebelMouse

This environment is using Python and MongoDB.
To run it you will need docker installed

# Getting started

## OSX and Linux

```bash
docker-compose up --build
```

## Windows 10

```bash
docker-compose.exe up --build
```
Scripts code can be found in: `/src/`

Default entrypoint without any parameters: `/src/script.py`

Your data dump should be placed into: `/data/`

Place your account credentials: `/docker.env`
