import { Col, Icon, Row, Tooltip } from 'antd';
import React from 'react';
import numeral from 'numeral';
import { ChartCard, MiniArea, MiniBar, MiniProgress, Field } from './Charts';
import Trend from './Trend';
import Yuan from '../utils/Yuan';
import styles from '../style.less';

const topColResponsiveProps = {
  xs: 24,
  sm: 12,
  md: 12,
  lg: 12,
  xl: 6,
  style: {
    marginBottom: 24,
  },
};

const IntroduceRow = ({ loading, visitData }) => (
  <Row gutter={24} type="flex">
    <Col {...topColResponsiveProps}>
      <ChartCard
        bordered={false}
        title="总用户数"
        loading={loading}
        total={numeral(16560).format('0,0')}
        footer={<Field label="日增用户数" value={`${numeral(23).format('0,0')}`} />}
        contentHeight={46}
      >
        <Trend
          flag="up"
          style={{
            marginRight: 16,
          }}
        >
          周同比
          <span className={styles.trendText}>12%</span>
        </Trend>
        <Trend flag="up">
          日同比
          <span className={styles.trendText}>11%</span>
        </Trend>
      </ChartCard>
    </Col>

    <Col {...topColResponsiveProps}>
      <ChartCard
        bordered={false}
        loading={loading}
        title="访问量"
        total={numeral(8846).format('0,0')}
        footer={<Field label="日访问量" value={numeral(1234).format('0,0')} />}
        contentHeight={46}
      >
        <MiniArea color="#975FE4" data={visitData} />
      </ChartCard>
    </Col>
    <Col {...topColResponsiveProps}>
      <ChartCard
        bordered={false}
        loading={loading}
        title="新增视频数（月度）"
        action={
          <Tooltip title="图例为每日新增视频数">
            <Icon type="info-circle-o" />
          </Tooltip>
        }
        total={numeral(656).format('0,0')}
        footer={
          <div
            style={{
              whiteSpace: 'nowrap',
              overflow: 'hidden',
            }}
          >
            <Trend
              flag="up"
              style={{
                marginRight: 16,
              }}
            >
              周同比
              <span className={styles.trendText}>15%</span>
            </Trend>
            <Trend flag="down">
              日同比
              <span className={styles.trendText}>13%</span>
            </Trend>
          </div>
        }
        contentHeight={46}
      >
        <MiniBar data={visitData} />
      </ChartCard>
    </Col>
    <Col {...topColResponsiveProps}>
      <ChartCard
        bordered={false}
        loading={loading}
        title="新增文章数（月度）"
        action={
          <Tooltip title="图例为每日新增文章数">
            <Icon type="info-circle-o" />
          </Tooltip>
        }
        total={numeral(352).format('0,0')}
        footer={
          <div
            style={{
              whiteSpace: 'nowrap',
              overflow: 'hidden',
            }}
          >
            <Trend
              flag="up"
              style={{
                marginRight: 16,
              }}
            >
              周同比
              <span className={styles.trendText}>5%</span>
            </Trend>
            <Trend flag="down">
              日同比
              <span className={styles.trendText}>7%</span>
            </Trend>
          </div>
        }
        contentHeight={46}
      >
        <MiniBar data={visitData} />
      </ChartCard>
    </Col>
    {/* <Col {...topColResponsiveProps}>
      <ChartCard
        loading={loading}
        bordered={false}
        title="运营活动效果"
        action={
          <Tooltip title="指标说明">
            <Icon type="info-circle-o" />
          </Tooltip>
        }
        total="78%"
        footer={
          <div
            style={{
              whiteSpace: 'nowrap',
              overflow: 'hidden',
            }}
          >
            <Trend
              flag="up"
              style={{
                marginRight: 16,
              }}
            >
              周同比
              <span className={styles.trendText}>12%</span>
            </Trend>
            <Trend flag="down">
              日同比
              <span className={styles.trendText}>11%</span>
            </Trend>
          </div>
        }
        contentHeight={46}
      >
        <MiniProgress percent={78} strokeWidth={8} target={80} color="#13C2C2" />
      </ChartCard>
    </Col> */}
  </Row>
);

export default IntroduceRow;
