resource "aws_internet_gateway" "cloudops" {
  vpc_id = aws_vpc.cloudops.id

  tags = {
    Name = "igw-cloudops-dev"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.cloudops.id

  tags = {
    Name = "rt-cloudops-public"
  }
}

resource "aws_route" "public_internet" {
  route_table_id         = aws_route_table.public.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.cloudops.id
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  vpc_id = aws_vpc.cloudops.id

  tags = {
    Name = "rt-cloudops-private"
  }
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private.id
}
