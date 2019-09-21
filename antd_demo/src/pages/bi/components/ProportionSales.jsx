import { Card, Radio } from 'antd';
import React from 'react';
import { Pie } from './Charts';
import Yuan from '../utils/Yuan';
import styles from '../style.less';

const ProportionSales = ({
  dropdownGroup,
  salesType,
  loading,
  salesPieData,
  handleChangeSalesType,
}) => (
  <Card
    loading={loading}
    className={styles.salesCard}
    bordered={false}
    title="访问类别占比"
    style={{
      height: '100%',
    }}
  >
    <div>
      <h4
        style={{
          marginTop: 8,
          marginBottom: 32,
        }}
      >
        访问量
      </h4>
      <Pie
        hasLegend
        subTitle="访问量"
        total={salesPieData.reduce((pre, now) => now.y + pre, 0)}
        data={salesPieData}
        height={248}
        lineWidth={4}
      />
    </div>
  </Card>
);

export default ProportionSales;
