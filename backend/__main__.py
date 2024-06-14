if __name__ == "__main__":
  try:
    from api import main
    main()
  except KeyboardInterrupt:
    print("exiting...")
