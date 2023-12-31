
// Generated by Cadence Genus Synthesis Solution GENUS15.13 - 15.10-s038_1

// Verification Directory fv/top 

module top(next_state, cur_state, at_sendreg, at_senddmaa, at_sendpios,
     at_senddmas, at_sendbista, at_senddata, lk_txfsmidle, lk_txerror,
     r2t_waittxid, r2t_rxempty, txtimeout, expire, tptx_reset);
  input [14:0] cur_state;
  input at_sendreg, at_senddmaa, at_sendpios, at_senddmas,
       at_sendbista, at_senddata, lk_txfsmidle, lk_txerror,
       r2t_waittxid, r2t_rxempty, txtimeout, expire, tptx_reset;
  output [14:0] next_state;
  wire [14:0] cur_state;
  wire at_sendreg, at_senddmaa, at_sendpios, at_senddmas, at_sendbista,
       at_senddata, lk_txfsmidle, lk_txerror, r2t_waittxid,
       r2t_rxempty, txtimeout, expire, tptx_reset;
  wire [14:0] next_state;
  wire n_629, n_631, n_633, n_641, n_676, n_677, n_678, n_679;
  wire n_680, n_681, n_682, n_683, n_684, n_685, n_686, n_687;
  wire n_688, n_689, n_690, n_780, n_782, n_783, n_794, n_795;
  wire n_826, n_827, n_828, n_829, n_831, n_832, n_833, n_834;
  wire n_835, n_836, n_837, n_838, n_839, n_840, n_841, n_842;
  wire n_843, n_844, n_845, n_846, n_847, n_848, n_849, n_850;
  wire n_857, n_861, n_865, n_866, n_871, n_874, n_879, n_887;
  wire n_895, n_904, n_912, n_920, n_928, n_937, n_945, n_960;
  wire n_967, n_977, n_987, n_988, n_992, n_995, n_1017, n_1041;
  wire n_1066, n_1101, n_1102, n_1179, n_1231, n_1277, n_1278, n_1280;
  wire n_1368, n_1369, n_1580, n_1582, n_1589, n_1592, n_1593, n_1596;
  wire n_1597, n_1600, n_1601, n_1604, n_1607, n_1609, n_1611, n_1614;
  wire n_1615, n_1618, n_1619, n_1622, n_1623, n_1626, n_1627, n_1668;
  wire n_1669, n_1670, n_1671, n_1672, n_1673, n_1674, n_1675, n_1676;
  wire n_1677, n_1678, n_1679, n_1680, n_1681, n_1682, n_1683, n_1684;
  wire n_1685, n_1686, n_1687, n_1688, n_1689, n_1690, n_1691, n_1692;
  wire n_1693, n_1694, n_1695, n_1696, n_1697, n_1698, n_1699, n_1700;
  wire n_1701, n_1702, n_1703, n_1704, n_1705, n_1706, n_1707, n_1708;
  wire n_1709, n_1710, n_1711, n_1712, n_1713, n_1714, n_1715, n_1716;
  wire n_1717, n_1718, n_1719, n_1720, n_1721, n_1722, n_1723, n_1724;
  wire n_1725, n_1726, n_1727, n_1728, n_1729, n_1730, n_1731, n_1732;
  wire n_1733, n_1734, n_1735, n_1736, n_1737, n_1738, n_1739, n_1740;
  wire n_1741, n_1742, n_1743, n_1744, n_1745, n_1746, n_1747, n_1748;
  wire n_1749, n_1750, n_1751, n_1752, n_1753, n_1754, n_1755, n_1756;
  wire n_1757, n_1758, n_1759, n_1760, n_1761, n_1762, n_1763, n_1764;
  wire n_1765, n_1766, n_1767, n_1768, n_1769, n_1770, n_1771, n_1772;
  nor g112 (n_690, n_845, n_827, n_828, n_834);
  nor g110 (n_689, n_844, n_827, n_828, n_834);
  nor g102 (n_685, n_826, n_840, n_828, n_834);
  nor g104 (n_686, n_826, n_841, n_828, n_834);
  nor g106 (n_687, n_842, n_827, n_828, n_834);
  nor g108 (n_688, n_843, n_827, n_828, n_834);
  nor g92 (n_680, n_826, n_827, n_835, n_834);
  nor g94 (n_681, n_826, n_827, n_836, n_834);
  nor g96 (n_682, n_826, n_827, n_837, n_834);
  nor g98 (n_683, n_826, n_838, n_828, n_834);
  nor g83 (n_676, n_826, n_827, n_828, n_829);
  nor g85 (n_677, n_826, n_827, n_828, n_831);
  nor g87 (n_678, n_826, n_827, n_828, n_832);
  nor g90 (n_679, n_826, n_827, n_833, n_834);
  nor g100 (n_684, n_826, n_839, n_828, n_834);
  nand g117 (n_850, n_846, n_847, n_848, n_849);
  nor g116 (n_849, n_688, n_689, n_690);
  nor g115 (n_848, n_684, n_685, n_686, n_687);
  nor g114 (n_847, n_680, n_681, n_682, n_683);
  nor g113 (n_846, n_676, n_677, n_678, n_679);
  nor g76 (n_794, at_senddmas, at_senddmaa, at_sendbista, at_senddata);
  nor g719 (n_641, lk_txfsmidle, txtimeout);
  nand g739 (n_780, lk_txfsmidle, r2t_rxempty);
  nor g772 (n_967, n_850, tptx_reset);
  nor g801 (n_1369, n_641, lk_txfsmidle);
  nor g802 (n_1368, n_641, lk_txerror);
  not g1440 (n_1668, at_senddata);
  not g1441 (n_1669, at_sendbista);
  not g1442 (n_1670, at_senddmaa);
  not g1443 (n_1671, at_senddmas);
  not g1444 (n_1672, lk_txfsmidle);
  not g1445 (n_1673, r2t_rxempty);
  not g1446 (n_1674, tptx_reset);
  not g1447 (n_1675, lk_txerror);
  not g1448 (n_1676, expire);
  not g1449 (n_1677, cur_state[11]);
  not g1450 (n_1678, cur_state[12]);
  not g1451 (n_1679, cur_state[13]);
  not g1452 (n_1680, cur_state[14]);
  not g1453 (n_1681, cur_state[7]);
  not g1454 (n_1682, cur_state[8]);
  not g1455 (n_1683, cur_state[9]);
  not g1456 (n_1684, cur_state[10]);
  not g1457 (n_1685, cur_state[3]);
  not g1458 (n_1686, cur_state[4]);
  not g1459 (n_1687, cur_state[5]);
  not g1460 (n_1688, cur_state[6]);
  not g1461 (n_1689, cur_state[0]);
  not g1462 (n_1690, cur_state[1]);
  not g1463 (n_1691, cur_state[2]);
  not g1464 (n_1692, at_sendpios);
  not g1465 (n_1693, at_sendreg);
  not g1466 (n_1694, r2t_waittxid);
  nand g1467 (n_845, cur_state[14], n_1679, n_1678, n_1677);
  nand g1468 (n_827, n_1684, n_1683, n_1682, n_1681);
  nand g1469 (n_828, n_1688, n_1687, n_1686, n_1685);
  nand g1470 (n_834, n_1691, n_1690, n_1689);
  not g1471 (n_1695, n_690);
  nand g1472 (n_844, n_1680, cur_state[13], n_1678, n_1677);
  not g1473 (n_1696, n_689);
  nand g1474 (n_826, n_1680, n_1679, n_1678, n_1677);
  nand g1475 (n_840, n_1684, cur_state[9], n_1682, n_1681);
  not g1476 (n_1697, n_685);
  nand g1477 (n_841, cur_state[10], n_1683, n_1682, n_1681);
  not g1478 (n_1698, n_686);
  nand g1479 (n_842, n_1680, n_1679, n_1678, cur_state[11]);
  not g1480 (n_1699, n_687);
  nand g1481 (n_843, n_1680, n_1679, cur_state[12], n_1677);
  not g1482 (n_1700, n_688);
  nand g1483 (n_835, n_1688, n_1687, cur_state[4], n_1685);
  not g1484 (n_1701, n_680);
  nand g1485 (n_836, n_1688, cur_state[5], n_1686, n_1685);
  not g1486 (n_1702, n_681);
  nand g1487 (n_837, cur_state[6], n_1687, n_1686, n_1685);
  not g1488 (n_1703, n_682);
  nand g1489 (n_838, n_1684, n_1683, n_1682, cur_state[7]);
  not g1490 (n_1704, n_683);
  nand g1491 (n_829, n_1691, n_1690, cur_state[0]);
  not g1492 (n_1705, n_676);
  nand g1493 (n_831, n_1691, cur_state[1], n_1689);
  not g1494 (n_1706, n_677);
  nand g1495 (n_832, cur_state[2], n_1690, n_1689);
  not g1496 (n_1707, n_678);
  nand g1497 (n_833, n_1688, n_1687, n_1686, cur_state[3]);
  not g1498 (n_1708, n_679);
  nand g1499 (n_839, n_1684, n_1683, cur_state[8], n_1681);
  not g1500 (n_1709, n_684);
  nor g1501 (n_865, n_1705, tptx_reset);
  not g1502 (n_1710, n_865);
  not g1503 (n_1711, n_780);
  nand g1504 (n_782, n_1711, n_1693, n_1692);
  not g1505 (n_1712, n_782);
  nand g1506 (n_783, n_1712, n_1670, n_1671);
  nor g1507 (n_633, n_783, at_sendbista, n_1668);
  not g1508 (n_1713, n_633);
  nor g1509 (next_state[7], n_1710, n_1713);
  not g1510 (n_1714, n_794);
  not g1511 (n_1715, n_641);
  not g1512 (n_1716, n_967);
  not g1513 (n_1717, n_1369);
  not g1514 (n_1718, n_1368);
  nor g1515 (n_987, n_1710, r2t_rxempty);
  not g1516 (n_1719, n_987);
  nor g1517 (n_866, n_1706, tptx_reset);
  not g1518 (n_1720, n_866);
  nor g1519 (n_1101, n_1720, r2t_waittxid);
  not g1520 (n_1721, n_1101);
  nand g1521 (next_state[1], n_1719, n_1721);
  nor g1522 (n_879, n_1695, tptx_reset);
  not g1523 (n_1722, n_879);
  nor g1524 (n_895, n_1696, tptx_reset);
  not g1525 (n_1723, n_895);
  nor g1526 (n_912, n_1700, tptx_reset);
  not g1527 (n_1724, n_912);
  nor g1528 (n_928, n_1699, tptx_reset);
  not g1529 (n_1725, n_928);
  nor g1530 (n_945, n_1698, tptx_reset);
  not g1531 (n_1726, n_945);
  nand g1532 (n_1231, n_1723, n_1724, n_1725, n_1726);
  not g1533 (n_1727, n_1231);
  nand g1534 (n_1280, n_1722, n_1727);
  not g1535 (n_1728, n_1280);
  nand g1536 (n_861, n_1717, n_1718);
  not g1537 (n_1729, n_861);
  nor g1538 (n_1580, n_1728, n_1729);
  not g1539 (n_1730, n_1580);
  nor g1540 (n_871, n_1703, tptx_reset);
  not g1541 (n_1731, n_871);
  nor g1542 (n_1582, n_1731, n_1676);
  not g1543 (n_1732, n_1582);
  nor g1544 (n_1589, n_1722, n_1715);
  not g1545 (n_1733, n_1589);
  nor g1546 (n_1592, n_1723, n_1715);
  not g1547 (n_1734, n_1592);
  nor g1548 (n_904, n_1701, tptx_reset);
  not g1549 (n_1735, n_904);
  nor g1550 (n_1593, n_1735, n_1676);
  not g1551 (n_1736, n_1593);
  nor g1552 (n_1596, n_1724, n_1715);
  not g1553 (n_1737, n_1596);
  nor g1554 (n_920, n_1708, tptx_reset);
  not g1555 (n_1738, n_920);
  nor g1556 (n_1597, n_1738, n_1676);
  not g1557 (n_1739, n_1597);
  nor g1558 (n_1600, n_1725, n_1715);
  not g1559 (n_1740, n_1600);
  nor g1560 (n_937, n_1707, tptx_reset);
  not g1561 (n_1741, n_937);
  nor g1562 (n_1601, n_1741, n_1676);
  not g1563 (n_1742, n_1601);
  nor g1564 (n_1604, n_1726, n_1715);
  not g1565 (n_1743, n_1604);
  nor g1566 (n_960, n_1709, tptx_reset);
  not g1567 (n_1744, n_960);
  nor g1568 (n_1609, n_1744, n_1676);
  not g1569 (n_1745, n_1609);
  nor g1570 (n_857, n_641, n_1672, n_1675);
  not g1571 (n_1746, n_857);
  nor g1572 (n_1611, n_1723, n_1746);
  not g1573 (n_1747, n_1611);
  nor g1574 (n_1615, n_1724, n_1746);
  not g1575 (n_1748, n_1615);
  nor g1576 (n_1619, n_1725, n_1746);
  not g1577 (n_1749, n_1619);
  nor g1578 (n_1623, n_1726, n_1746);
  not g1579 (n_1750, n_1623);
  nor g1580 (n_1627, n_1722, n_1746);
  not g1581 (n_1751, n_1627);
  nand g1582 (next_state[14], n_1732, n_1733);
  nor g1583 (n_887, n_1702, tptx_reset);
  not g1584 (n_1752, n_887);
  nand g1585 (next_state[13], n_1752, n_1734);
  nand g1586 (next_state[12], n_1736, n_1737);
  nand g1587 (next_state[11], n_1739, n_1740);
  nand g1588 (next_state[10], n_1742, n_1743);
  nor g1589 (n_977, n_1704, tptx_reset);
  not g1590 (n_1753, n_977);
  nor g1591 (n_1607, n_1744, expire);
  not g1592 (n_1754, n_1607);
  nand g1593 (next_state[8], n_1753, n_1754);
  nand g1594 (next_state[9], n_1745, n_1716);
  nor g1595 (n_631, n_782, n_1670, at_senddmas);
  not g1596 (n_1755, n_631);
  nor g1597 (n_992, n_1755, n_1710);
  not g1598 (n_1756, n_992);
  nand g1599 (next_state[5], n_1756, n_1747);
  nor g1600 (n_1017, n_782, n_1710, n_1671);
  not g1601 (n_1757, n_1017);
  nor g1602 (n_1614, n_1735, expire);
  not g1603 (n_1758, n_1614);
  nand g1604 (next_state[4], n_1757, n_1758, n_1748);
  nor g1605 (n_629, n_780, at_sendreg, n_1692);
  not g1606 (n_1759, n_629);
  nor g1607 (n_1041, n_1759, n_1710);
  not g1608 (n_1760, n_1041);
  nor g1609 (n_1618, n_1738, expire);
  not g1610 (n_1761, n_1618);
  nand g1611 (next_state[3], n_1760, n_1761, n_1749);
  nor g1612 (n_1066, n_780, n_1710, n_1693);
  not g1613 (n_1762, n_1066);
  nor g1614 (n_1622, n_1741, expire);
  not g1615 (n_1763, n_1622);
  nand g1616 (next_state[2], n_1762, n_1763, n_1750);
  nor g1617 (n_1179, n_1710, n_783, n_1669);
  not g1618 (n_1764, n_1179);
  nor g1619 (n_1626, n_1731, expire);
  not g1620 (n_1765, n_1626);
  nand g1621 (next_state[6], n_1764, n_1765, n_1751);
  nor g1622 (n_874, n_1697, tptx_reset);
  not g1623 (n_1766, n_874);
  nor g1624 (n_988, n_1710, lk_txfsmidle, n_1673);
  not g1625 (n_1767, n_988);
  nor g1626 (n_795, at_sendreg, at_sendpios, n_1672, n_1673);
  not g1627 (n_1768, n_795);
  nor g1628 (n_995, n_1714, n_1768, n_1710);
  not g1629 (n_1769, n_995);
  nor g1630 (n_1102, n_1720, n_1694);
  not g1631 (n_1770, n_1102);
  nand g1632 (n_1277, n_1766, n_1767, n_1769, n_1770);
  not g1633 (n_1771, n_1277);
  nand g1634 (n_1278, n_1771, n_1674);
  not g1635 (n_1772, n_1278);
  nand g1636 (next_state[0], n_1772, n_1730);
endmodule

