<!--
SPDX-License-Identifier: MIT
Copyright (c) 2020 The Authors.

Authors: Sherif Abdelwahab <@zasherif>
         Phu Tran          <@phudtran>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:The above copyright
notice and this permission notice shall be included in all copies or
substantial portions of the Software.THE SOFTWARE IS PROVIDED "AS IS",
WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR
THE USE OR OTHER DEALINGS IN THE SOFTWARE.
-->

Welcome to Mizar - the open-source high-performance cloud-network powered by [ eXpress Data Path (XDP)](https://prototype-kernel.readthedocs.io/en/latest/networking/XDP/) and [Geneve protocol](https://tools.ietf.org/html/draft-ietf-nvo3-geneve-08) for high scale cloud.

Mizar is a simple and efficient solution that lets you create a multi-tenant overlay network of a massive number of endpoints with extensible network functions that:

* Support provisioning and management of enormous number endpoints
* Accelerate network resource provisioning for dynamic cloud environments
* Achieve high network throughput and low latency
* Create an extensible cloud-network of pluggable network functions
* Unify the network data-plane for containers, serverless functions, virtual machines, etc
* Isolate multi-tenant's traffic and address space

## What is Mizar?

We think of Mizar as a server-less platform for networking functions, in which developers extend it with capabilities without compromising performance or scale.

The following diagram illustrates Mizar's high-level architecture:

![Mizar Overview](design/png/overall_mgmt_dp.png)

Mizar's [data-plane](design/dp_overview.md) provides high performance and extensible packet processing pipeline and functions that achieve Mizar's functional, scale, and performance goals. Mizar's [management-plane](design/mp_overview.md) programs the data-plane by translating typical networking related APIs and resources to Mizar specific configuration. The programmability of the data-plane involves loading and unloading network functions at various stages of the packet processing pipeline.

## Why Mizar is different?

Unlike traditional networking solutions, Mizar relies on the natural partitioning of a cloud network to scale. Mizar simplifies the programming of data-plane to scale by flexible in-network processing, compared to flow-based programming models. As it primarily targets use cases of cloud-networking among virtual machines and containers, Mizar reduces the control-plane overhead of several routing and switching protocols within a cloud environment (e.g., L2 learning, ARP, BGP, etc.).

The following diagram illustrates the overall logical architecture of Mizar:

![Mizar Overview](design/png/Mizar.png)

* Virtual Private Cloud (VPC) domain: A flat-network of endpoints specific to a single tenant.
* Networks within a VPC: a group of Endpoints within a VPC. An operator may identify Networks as subnets of the VPC address space or any other partitioning scheme.
* Endpoint within a Network: the group of endpoints forming a network. Endpoints of a network have IP addresses from the VPC address space and need not have IP address of one subnet.

Traditionally routing between VPCs and subnets is managed by virtual switches and routers. These mandates, for example, that endpoints belong to the same subnets, and a network of endpoints must have a subnet address. Mizar does not have this restriction.

Mizar, introduces new **abstract** components called **Bouncers** and **Dividers**. Bouncers and Dividers are in-network and horizontally scalable hash tables. The management-plane populates the Bouncers and Dividers tables according to network domain partitioning.

Bouncers' decision domain is constrained to a network. A Bouncer holds the configuration of endpoints within a network. When a packet arrives at a Bouncer, it is expected to find the destination endpoint's host and __bounce__ the packet back to the host. Unlike a switch - where packet forwarding is performed by L2 learning - Bouncer's configuration maintains a mapping of an endpoint within a VPC to its host. The endpoint is identified by its IP address within a VPC (VNI). Bouncers rewrite the destination IP address of the outer packet to the endpoint's host.

Dividers' decision domain is constrained to VPCs. A Divider holds the configuration of all networks within a VPC; hence it divides (shards) the traffic inside the VPC across multiple bouncers. Dividers do not maintain endpoint-to-host mapping information. When a divider receives a packet, it determines which bouncer has the host information of the destination endpoint **according to the network partitioning logic** and rewrites the destination IP of the outer packet to the bouncer.

This overall architecture allows - among many advantages - to accelerate endpoints provisioning, as the management plane programs a finite number of hosts designated as Bouncers instead of propagating the endpoint configuration to each host.


To learn more about Mizar design:

* [Data-plane](design/dp_overview.md)
* [Management Plane](design/mp_overview.md)
