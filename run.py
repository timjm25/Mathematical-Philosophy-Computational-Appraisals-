from mdn.app import create_app

if __name__ == "__main__":
    create_app("mdn.db").run(host="127.0.0.1", port=5075, debug=False)
