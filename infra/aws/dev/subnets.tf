data "aws_availability_zones" "available" {
  state = "available"

  filter {
    name   = "zone-type"
    values = ["availability-zone"]
  }
}

locals {
  azs = slice(data.aws_availability_zones.available.names, 0, 2)
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.cloudops.id
  availability_zone       = local.azs[count.index]
  cidr_block              = "10.30.${count.index + 1}.0/24"
  map_public_ip_on_launch = false

  tags = {
    Name = "snet-cloudops-public-${count.index + 1}"
    Tier = "public"
  }
}

resource "aws_subnet" "private" {
  count                   = 2
  vpc_id                  = aws_vpc.cloudops.id
  availability_zone       = local.azs[count.index]
  cidr_block              = "10.30.${count.index + 11}.0/24"
  map_public_ip_on_launch = false

  tags = {
    Name = "snet-cloudops-private-${count.index + 1}"
    Tier = "private"
  }
}
