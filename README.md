# Introduction

Đây là một chương trình mô phỏng luồng hoạt động trong việc xử lý dữ liệu đồng cấu. (Homomorphic Encryption)

## Installation

Project này sử dụng **devcontainer** để khởi tạo môi trường. Editor khuyên dùng là **VS Code** với extension **Dev Containers**

## Architecture

Project này bao gồm 2 thành phần: *homomorphic client* dùng để mô phỏng các thao tác người dùng sẽ làm để bảo mật dữ liệu gửi đi và *homomorphic server* dùng để mô phỏng cách server xử lý dữ liệu bảo mật mà không làm mất đi tính toàn vẹn và riêng tư của chúng.

## Generate gRPC

Nếu có bất kỳ thay đổi nào về cấu trúc proto, hãy chạy lại câu lệnh sau:

```bash
./generate.sh
```

## Usage

### Homomorphic Server

```bash
python3 -m homomorphic_server.main
```

### Homomorphic Client

```bash
python3 -m homomorphic_client.main  --data 100 100 50 --op +
```

## License

[MIT](https://choosealicense.com/licenses/mit/)